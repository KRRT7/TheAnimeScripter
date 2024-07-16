import logging
import subprocess
import os
import shutil
import torch
import sys

from queue import Queue

if os.name == "nt":
    appdata = os.getenv("APPDATA")
    mainPath = os.path.join(appdata, "TheAnimeScripter")
    
    if not os.path.exists(mainPath):
        os.makedirs(mainPath)
else:
    dirPath = os.path.dirname(os.path.realpath(__file__))

ffmpegLogPath = os.path.join(mainPath, "ffmpegLog.txt")

if getattr(sys, "frozen", False):
    outputPath = os.path.dirname(sys.executable)
else:
    outputPath = os.path.dirname(os.path.abspath(__file__))

def matchEncoder(encode_method: str):
    """
    encode_method: str - The method to use for encoding the video. Options include "x264", "x264_animation", "nvenc_h264", etc.
    """
    command = []
    match encode_method:
        case "x264":
            command.extend(["-c:v", "libx264", "-preset", "veryfast", "-crf", "15"])
        case "x264_10bit":
            command.extend(["-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-profile:v", "high10"])
        case "x264_animation":
            command.extend(
                [
                    "-c:v",
                    "libx264",
                    "-preset",
                    "veryfast",
                    "-tune",
                    "animation",
                    "-crf",
                    "15",
                ]
            )
        case "x264_animation_10bit":
            command.extend(
                [
                    "-c:v",
                    "libx264",
                    "-preset",
                    "veryfast",
                    "-tune",
                    "animation",
                    "-crf",
                    "15",
                    "-profile:v",
                    "high10",
                ]
            )
        case "x265":
            command.extend(["-c:v", "libx265", "-preset", "veryfast", "-crf", "15"])
        case "x265_10bit":
            command.extend(["-c:v", "libx265", "-preset", "veryfast", "-crf", "15", "-profile:v", "main10"])
        case "nvenc_h264":
            command.extend(["-c:v", "h264_nvenc", "-preset", "p1", "-cq", "15"])
        case "nvenc_h265":
            command.extend(["-c:v", "hevc_nvenc", "-preset", "p1", "-cq", "15"])
        case "nvenc_h265_10bit":
            command.extend(["-c:v", "hevc_nvenc", "-preset", "p1", "-cq", "15", "-profile:v", "main10"])
        case "qsv_h264":
            command.extend(
                ["-c:v", "h264_qsv", "-preset", "veryfast", "-global_quality", "15"]
            )
        case "qsv_h265":
            command.extend(
                ["-c:v", "hevc_qsv", "-preset", "veryfast", "-global_quality", "15"]
            )
        case "qsv_h265_10bit":
            command.extend(
                ["-c:v", "hevc_qsv", "-preset", "veryfast", "-global_quality", "15", "-profile:v", "main10"]
            )
        case "nvenc_av1":
            command.extend(["-c:v", "av1_nvenc", "-preset", "p1", "-cq", "15"])
        case "av1":
            command.extend(["-c:v", "libsvtav1", "-preset", "8", "-crf", "15"])
        case "h264_amf":
            command.extend(
                ["-c:v", "h264_amf", "-quality", "speed", "-rc", "cqp", "-qp", "15"]
            )
        case "hevc_amf":
            command.extend(
                ["-c:v", "hevc_amf", "-quality", "speed", "-rc", "cqp", "-qp", "15"]
            )
        case "hevc_amf_10bit":
            command.extend(
                ["-c:v", "hevc_amf", "-quality", "speed", "-rc", "cqp", "-qp", "15", "-profile:v", "main10"]
            )
        # Needs further testing, -qscale:v 15 seems to be extremely lossy
        case "prores":
            command.extend(["-c:v", "prores_ks", "-profile:v", "4", "-qscale:v", "15"])
        
    return command


class BuildBuffer:
    def __init__(
        self,
        input: str = "",
        ffmpegPath: str = "",
        inpoint: float = 0.0,
        outpoint: float = 0.0,
        dedup: bool = False,
        dedupSens: float = 0.0,
        dedupMethod: str = "ssim",
        width: int = 1920,
        height: int = 1080,
        resize: bool = False,
        resizeMethod: str = "bilinear",
        buffSize: int = 10**8,
        queueSize: int = 50,
        totalFrames: int = 0,
    ):
        """
        A class meant to Pipe the Output of FFMPEG into a Queue for further processing.

        input: str - The path to the input video file.
        ffmpegPath: str - The path to the FFmpeg executable.
        inpoint: float - The start time of the segment to decode, in seconds.
        outpoint: float - The end time of the segment to decode, in seconds.
        dedup: bool - Whether to apply a deduplication filter to the video.
        dedupSens: float - The sensitivity of the deduplication filter.
        width: int - The width of the output video in pixels.
        height: int - The height of the output video in pixels.
        resize: bool - Whether to resize the video.
        resizeMethod: str - The method to use for resizing the video. Options include: "fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos",
        "spline",
        buffSize: int - The size of the subprocess buffer in bytes, don't touch unless you are working with some ginormous 8K content.
        queueSize: int - The size of the queue.
        """
        self.input = os.path.normpath(input)
        self.ffmpegPath = os.path.normpath(ffmpegPath)
        self.inpoint = inpoint
        self.outpoint = outpoint
        self.dedup = dedup
        self.dedupSens = dedupSens
        self.dedupeMethod = dedupMethod
        self.resize = resize
        self.width = width
        self.height = height
        self.resizeMethod = resizeMethod
        self.buffSize = buffSize
        self.queueSize = queueSize
        self.totalFrames = totalFrames

    def decodeSettings(self) -> list:
        """
        This returns a command for FFMPEG to work with, it will be used inside of the scope of the class.

        input: str - The path to the input video file.
        inpoint: float - The start time of the segment to decode, in seconds.
        outpoint: float - The end time of the segment to decode, in seconds.
        dedup: bool - Whether to apply a deduplication filter to the video.
        dedup_strenght: float - The strength of the deduplication filter.
        ffmpegPath: str - The path to the FFmpeg executable.
        resize: bool - Whether to resize the video.
        resizeMethod: str - The method to use for resizing the video. Options include: "fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos",
        "spline",
        """
        command = [
            self.ffmpegPath,
        ]

        if self.outpoint != 0:
            command.extend(["-ss", str(self.inpoint), "-to", str(self.outpoint)])

        command.extend(
            [
                "-i",
                self.input,
            ]
        )

        filters = []
        if self.resize:
            if self.resizeMethod in ["spline16", "spline36", "point"]:
                filters.append(
                    f"zscale={self.width}:{self.height}:filter={self.resizeMethod}"
                )
            else:
                filters.append(
                    f"scale={self.width}:{self.height}:flags={self.resizeMethod}"
                )

        if filters:
            command.extend(["-vf", ",".join(filters)])

        command.extend(
            [
                "-f",
                "image2pipe",
                "-pix_fmt",
                "rgb24",
                '-vcodec', 
                'rawvideo',
                '-'
            ]
        )

        return command

    def start(self, queue: Queue = None):
        """
        The actual underlying logic for decoding, it starts a queue and gets the necessary FFMPEG command from decodeSettings.
        This is meant to be used in a separate thread for faster processing.

        queue : queue.Queue, optional - The queue to put the frames into. If None, a new queue will be created.
        verbose : bool - Whether to log the progress of the decoding.
        """
        self.readBuffer = queue if queue is not None else Queue(maxsize=self.queueSize)
        verbose = True
        command = self.decodeSettings()

        if verbose:
            logging.info(f"Decoding options: {' '.join(map(str, command))}")
            
        try:
            chunk = self.width * self.height * 3
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            self.decodedFrames = 0
            self.readingDone = False

            for _ in range(self.totalFrames):
                raw_frame = process.stdout.read(chunk)
                self.readBuffer.put(torch.frombuffer(raw_frame, dtype=torch.uint8).view(self.height, self.width, 3))
                self.decodedFrames += 1
                
        except Exception as e:
            if verbose:
                logging.error(f"An error occurred: {str(e)}")
        finally:
            if verbose:
                logging.info(f"Built buffer with {self.decodedFrames} frames")
            self.readingDone = True
            self.readBuffer.put(None)
            process.stdout.close()
            
    def read(self):
        """
        Returns a numpy array in RGB format.
        """
        return self.readBuffer.get()

    def isReadingDone(self):
        """
        Check if the reading is done, safelock for the queue environment.
        """
        return self.readingDone

    def getDecodedFrames(self):
        """
        Get the amount of processed frames.
        """
        return self.decodedFrames

    def getSizeOfQueue(self):
        """
        Get the size of the queue.
        """
        return self.readBuffer.qsize()
    
    def getTotalFrames(self):
        """
        Get the total amount of frames.
        """
        return self.totalFrames


class WriteBuffer:
    def __init__(
        self,
        input: str = "",
        output: str = "",
        ffmpegPath: str = "",
        encode_method: str = "x264",
        custom_encoder: str = "",
        width: int = 1920,
        height: int = 1080,
        fps: float = 60.0,
        queueSize: int = 50,
        sharpen: bool = False,
        sharpen_sens: float = 0.0,
        grayscale: bool = False,
        transparent: bool = False,
        audio: bool = True,
        benchmark: bool = False,
    ):
        """
        A class meant to Pipe the input to FFMPEG from a queue.

        output: str - The path to the output video file.
        ffmpegPath: str - The path to the FFmpeg executable.
        encode_method: str - The method to use for encoding the video. Options include "x264", "x264_animation", "nvenc_h264", etc.
        custom_encoder: str - A custom encoder string to use for encoding the video.
        grayscale: bool - Whether to encode the video in grayscale.
        width: int - The width of the output video in pixels.
        height: int - The height of the output video in pixels.
        fps: float - The frames per second of the output video.
        sharpen: bool - Whether to apply a sharpening filter to the video.
        sharpen_sens: float - The sensitivity of the sharpening filter.
        queueSize: int - The size of the queue.
        transparent: bool - Whether to encode the video with transparency.
        audio: bool - Whether to include audio in the output video.
        benchmark: bool - Whether to benchmark the encoding process, this will not output any video.
        """
        self.input = input
        self.output = os.path.normpath(output)
        self.ffmpegPath = os.path.normpath(ffmpegPath)
        self.encode_method = encode_method
        self.custom_encoder = custom_encoder
        self.grayscale = grayscale
        self.width = width
        self.height = height
        self.fps = fps
        self.sharpen = sharpen
        self.sharpen_sens = sharpen_sens
        self.queueSize = queueSize
        self.transparent = transparent
        self.audio = audio
        self.benchmark = benchmark

    def encodeSettings(self, verbose: bool = False) -> list:
        """
        This will return the command for FFMPEG to work with, it will be used inside of the scope of the class.

        verbose : bool - Whether to log the progress of the encoding.
        """

        if self.transparent:
            if self.encode_method not in ["prores", "prores_ks"]:
                if verbose:
                    logging.info(
                        "Switching internally to prores for transparency support"
                    )
                self.encode_method = "prores"

            inputPixFormat = "rgba"
            outputPixFormat = "yuva444p10le"

        elif self.grayscale:
            inputPixFormat = "gray"
            outputPixFormat = "yuv420p10le"

        elif self.encode_method in ["x264_10bit", "x265_10bit"]:
            inputPixFormat = "rgb24"
            outputPixFormat = "yuv420p10le"
        
        elif self.encode_method in ["nvenc_h265_10bit",  "hevc_amf_10bit", "qsv_h265_10bit"]:
            inputPixFormat = "rgb24"
            outputPixFormat = "p010le"
        else:
            inputPixFormat = "rgb24"
            outputPixFormat = "yuv420p"

        if not self.benchmark:
            command = [
                self.ffmpegPath,
                "-y",
                "-v",
                "warning",
                "-stats",
                "-f",
                "rawvideo",
                "-vcodec",
                "rawvideo",
                "-s",
                f"{self.width}x{self.height}",
                "-pix_fmt",
                f"{inputPixFormat}",
                "-r",
                str(self.fps),
                "-i",
                "-",
                "-an",
                "-fps_mode",
                "cfr",
            ]

            if not self.custom_encoder:
                command.extend(matchEncoder(self.encode_method))

                filters = []
                if self.sharpen:
                    filters.append("cas={}".format(self.sharpen_sens))
                if self.grayscale:
                    filters.append("format=gray")
                if self.transparent:
                    filters.append("format=rgba")
                if filters:
                    command.extend(["-vf", ",".join(filters)])

                command.extend(["-pix_fmt", outputPixFormat, self.output])

            else:
                customEncoderList = self.custom_encoder.split()

                if "-vf" in customEncoderList:
                    vf_index = customEncoderList.index("-vf")

                    if self.sharpen:
                        customEncoderList[vf_index + 1] += ",cas={}".format(
                            self.sharpen_sens
                        )

                    if self.grayscale:
                        customEncoderList[vf_index + 1] += ",format=gray"

                    if self.transparent:
                        customEncoderList[vf_index + 1] += ",format=rgba"
                else:
                    filters = []
                    if self.sharpen:
                        filters.append("cas={}".format(self.sharpen_sens))
                    if self.grayscale:
                        filters.append("format=gray")
                    if self.transparent:
                        filters.append("format=rgba")
                    if filters:
                        customEncoderList.extend(["-vf", ",".join(filters)])

                if "-pix_fmt" not in customEncoderList:
                    logging.info(f"-pix_fmt was not found in the custom encoder list, adding {outputPixFormat}, for future reference, it is recommended to add it.")
                    customEncoderList.extend(["-pix_fmt", outputPixFormat])

                command.extend(customEncoderList)

        else:
            # This is for benchmarking purposes,
            # it will not output any video and should be as low overhead as possible, I think.
            command = [
                self.ffmpegPath,
                "-y",
                "-v",
                "warning",
                "-stats",
                "-f",
                "rawvideo",
                "-vcodec",
                "rawvideo",
                "-s",
                f"{self.width}x{self.height}",
                "-pix_fmt",
                f"{inputPixFormat}",
                "-r",
                str(self.fps),
                "-i",
                "-",
                "-benchmark",
                "-f",
                "null",
                "-",
            ]

        return command

    def start(self, queue: Queue = None):
        """
        The actual underlying logic for encoding, it starts a queue and gets the necessary FFMPEG command from encodeSettings.
        This is meant to be used in a separate thread for faster processing.

        verbose : bool - Whether to log the progress of the encoding.
        queue : queue.Queue, optional - The queue to get the frames
        """
        verbose: bool = True
        command = self.encodeSettings(verbose=verbose)

        self.writeBuffer = queue if queue is not None else Queue(maxsize=self.queueSize)

        if verbose:
            logging.info(f"Encoding options: {' '.join(map(str, command))}")

        try:
            with open(ffmpegLogPath, 'w') as log_file:
                with subprocess.Popen(
                    command,
                    stdin=subprocess.PIPE,
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                ) as self.process:

                    writtenFrames = 0
                    self.isWritingDone = False
                    while True:
                        frame = self.writeBuffer.get()
                        if frame is None:
                            if verbose:
                                logging.info(f"Encoded {writtenFrames} frames")
                            break
                        
                        self.process.stdin.buffer.write(frame.contiguous().byte().cpu().numpy())
                        writtenFrames += 1

        except Exception as e:
            if verbose:
                logging.error(f"An error occurred: {str(e)}")

        finally:
            self.isWritingDone = True
            if self.audio and not self.benchmark:
                self.mergeAudio()

    def write(self, frame: torch.Tensor):
        """
        Add a frame to the queue. Must be in RGB format.
        """
        self.writeBuffer.put(frame)

    def close(self):
        """
        Close the queue.
        """
        self.writeBuffer.put(None)

    def mergeAudio(self):
        try:
            # Checking first if the clip has audio to begin with, if not we skip the audio merge
            ffmpegCommand = [
                self.ffmpegPath,
                "-i",
                self.input,
            ]
            result = subprocess.run(
                ffmpegCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if "Stream #0:1" not in result.stderr.decode():
                logging.info("No audio stream found, skipping audio merge")
                return

            audioFile = os.path.splitext(self.output)[0] + "_audio.aac"
            extractCommand = [
                self.ffmpegPath,
                "-v",
                "error",
                "-stats",
                "-i",
                self.input,
                "-vn",
                "-acodec",
                "copy",
                audioFile,
            ]
            subprocess.run(extractCommand)

            mergedFile = os.path.splitext(self.output)[0] + "_merged.mp4"

            ffmpegCommand = [
                self.ffmpegPath,
                "-v",
                "error",
                "-stats",
                "-i",
                audioFile,
                "-i",
                self.output,
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-map",
                "1:v:0",
                "-map",
                "0:a:0",
                "-shortest",
                "-y",
                mergedFile,
            ]

            logging.info(f"Merging audio with: {' '.join(ffmpegCommand)}")

            subprocess.run(ffmpegCommand)
            shutil.move(mergedFile, self.output)
            os.remove(audioFile)

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
