import os
import logging
import sys
import argparse

from urllib.parse import urlparse
from .generateOutput import outputNameGenerator
from .checkSpecs import checkSystem
from .getFFMPEG import getFFMPEG
from .ytdlp import VideoDownloader
from .downloadModels import downloadModels, modelsList
from .coloredPrints import green, red


def createParser(isFrozen, scriptVersion, mainPath, outputPath):
    argParser = argparse.ArgumentParser(
        description="The Anime Scripter CLI Tool",
        usage="main.py [options]" if not isFrozen else "main.exe [options]",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Basic options
    generalGroup = argParser.add_argument_group("General")
    generalGroup.add_argument("--version", action="version", version=f"{scriptVersion}")
    generalGroup.add_argument("--input", type=str, help="Input video file")
    generalGroup.add_argument("--output", type=str, help="Output video file")
    generalGroup.add_argument(
        "--inpoint", type=float, default=0, help="Input start time"
    )
    generalGroup.add_argument(
        "--outpoint", type=float, default=0, help="Input end time"
    )
    generalGroup.add_argument(
        "--preview", action="store_true", help="Preview the video during processing"
    )
    generalGroup.add_argument(
        "--hide_banner", action="store_true", help="Hide the TAS banner"
    )

    # Performance options
    performanceGroup = argParser.add_argument_group("Performance")
    performanceGroup.add_argument(
        "--half", type=bool, help="Use half precision for inference", default=True
    )

    # Interpolation options
    interpolationGroup = argParser.add_argument_group("Interpolation")
    interpolationGroup.add_argument(
        "--interpolate", action="store_true", help="Interpolate the video"
    )
    interpolationGroup.add_argument(
        "--interpolate_factor", type=float, default=2, help="Interpolation factor"
    )

    interpolationGroup.add_argument(
        "--interpolate_method",
        type=str,
        choices=[
            "rife",
            "rife4.6",
            "rife4.15-lite",
            "rife4.16-lite",
            "rife4.17",
            "rife4.18",
            "rife4.20",
            "rife4.21",
            "rife4.22",
            "rife4.22-lite",
            "rife-ncnn",
            "rife4.6-ncnn",
            "rife4.15-lite-ncnn",
            "rife4.16-lite-ncnn",
            "rife4.17-ncnn",
            "rife4.18-ncnn",
            "rife4.6-tensorrt",
            "rife4.15-lite-tensorrt",
            "rife4.17-tensorrt",
            "rife4.18-tensorrt",
            "rife4.20-tensorrt",
            "rife4.21-tensorrt",
            "rife4.22-tensorrt",
            "rife4.22-lite-tensorrt",
            "rife-tensorrt",
        ],
        default="rife",
        help="Interpolation method",
    )
    interpolationGroup.add_argument(
        "--ensemble",
        action="store_true",
        help="Use the ensemble model for interpolation",
    )

    # Upscaling options
    upscaleGroup = argParser.add_argument_group("Upscaling")
    upscaleGroup.add_argument(
        "--upscale", action="store_true", help="Upscale the video"
    )
    upscaleGroup.add_argument(
        "--upscale_factor", type=int, choices=[2], default=2, help="Upscaling factor"
    )
    upscaleGroup.add_argument(
        "--upscale_method",
        type=str,
        choices=[
            "shufflespan",
            "shufflecugan",
            "compact",
            "ultracompact",
            "superultracompact",
            "span",
            "compact-directml",
            "ultracompact-directml",
            "superultracompact-directml",
            "shufflespan-directml",
            "span-directml",
            "shufflecugan-ncnn",
            "span-ncnn",
            "compact-tensorrt",
            "ultracompact-tensorrt",
            "superultracompact-tensorrt",
            "span-tensorrt",
            "shufflecugan-tensorrt",
            "shufflespan-tensorrt",
            "open-proteus",
            "open-proteus-tensorrt",
            "open-proteus-directml",
            "aniscale2",
            "aniscale2-tensorrt",
            "aniscale2-directml",
        ],
        default="shufflecugan",
        help="Upscaling method",
    )
    upscaleGroup.add_argument(
        "--custom_model", type=str, default="", help="Path to custom upscaling model"
    )
    upscaleGroup.add_argument(
        "--upscale_skip",
        action="store_true",
        help="Use SSIM / SSIM-CUDA to skip duplicate frames when upscaling",
    )

    # Deduplication options
    dedupGroup = argParser.add_argument_group("Deduplication")
    dedupGroup.add_argument(
        "--dedup", action="store_true", help="Deduplicate the video"
    )
    dedupGroup.add_argument(
        "--dedup_method",
        type=str,
        default="ssim",
        choices=["ssim", "mse", "ssim-cuda", "mse-cuda"],
        help="Deduplication method",
    )
    dedupGroup.add_argument(
        "--dedup_sens", type=float, default=35, help="Deduplication sensitivity"
    )
    dedupGroup.add_argument(
        "--sample_size", type=int, default=224, help="Sample size for deduplication"
    )

    # Video processing options
    processingGroup = argParser.add_argument_group("Video Processing")
    processingGroup.add_argument(
        "--sharpen", action="store_true", help="Sharpen the video"
    )
    processingGroup.add_argument(
        "--sharpen_sens", type=float, default=50, help="Sharpening sensitivity"
    )
    processingGroup.add_argument(
        "--denoise", action="store_true", help="Denoise the video"
    )
    processingGroup.add_argument(
        "--denoise_method",
        type=str,
        default="scunet",
        choices=["scunet", "nafnet", "dpir", "real-plksr"],
        help="Denoising method",
    )
    processingGroup.add_argument(
        "--resize", action="store_true", help="Resize the video"
    )
    processingGroup.add_argument(
        "--resize_factor",
        type=float,
        default=2,
        help="Resize factor (can be between 0 and 1 for downscaling)",
    )
    processingGroup.add_argument(
        "--resize_method",
        type=str,
        choices=[
            "fast_bilinear",
            "bilinear",
            "bicubic",
            "experimental",
            "neighbor",
            "area",
            "bicublin",
            "gauss",
            "sinc",
            "lanczos",
            "point",
            "spline",
            "spline16",
            "spline36",
        ],
        default="bicubic",
        help="Resize method",
    )

    # Scene detection options
    sceneGroup = argParser.add_argument_group("Scene Detection")
    sceneGroup.add_argument("--segment", action="store_true", help="Segment the video")
    sceneGroup.add_argument(
        "--segment_method",
        type=str,
        default="anime",
        choices=["anime", "anime-tensorrt", "anime-directml"],
        help="Segmentation method",
    )
    sceneGroup.add_argument(
        "--autoclip", action="store_true", help="Detect scene changes"
    )
    sceneGroup.add_argument(
        "--autoclip_sens", type=float, default=50, help="Autoclip sensitivity"
    )
    sceneGroup.add_argument(
        "--scenechange", action="store_true", help="Detect scene changes"
    )
    sceneGroup.add_argument(
        "--scenechange_method",
        type=str,
        default="maxxvit-directml",
        choices=[
            "maxxvit-tensorrt",
            "maxxvit-directml",
            "differential",
            "differential-tensorrt",
            "shift_lpips-tensorrt",
            "shift_lpips-directml",
        ],
        help="Scene change detection method",
    )
    sceneGroup.add_argument(
        "--scenechange_sens",
        type=float,
        default=50,
        help="Scene change detection sensitivity (0-100)",
    )

    # Depth estimation options
    depthGroup = argParser.add_argument_group("Depth Estimation")
    depthGroup.add_argument(
        "--depth", action="store_true", help="Estimate the depth of the video"
    )
    depthGroup.add_argument(
        "--depth_method",
        type=str,
        choices=[
            "small_v2",
            "base_v2",
            "large_v2",
            "small_v2-tensorrt",
            "base_v2-tensorrt",
            "large_v2-tensorrt",
            "small_v2-directml",
            "base_v2-directml",
            "large_v2-directml",
        ],
        default="small_v2",
        help="Depth estimation method",
    )

    # Encoding options
    encodingGroup = argParser.add_argument_group("Encoding")
    encodingGroup.add_argument(
        "--encode_method",
        type=str,
        choices=[
            "x264",
            "x264_10bit",
            "x264_animation",
            "x264_animation_10bit",
            "x265",
            "x265_10bit",
            "nvenc_h264",
            "nvenc_h265",
            "nvenc_h265_10bit",
            "nvenc_av1",
            "qsv_h264",
            "qsv_h265",
            "qsv_h265_10bit",
            "av1",
            "h264_amf",
            "hevc_amf",
            "hevc_amf_10bit",
            "prores",
            "prores_segment",
            "gif",
            "image",
        ],
        default="x264",
        help="Encoding method",
    )
    encodingGroup.add_argument(
        "--custom_encoder", type=str, default="", help="Custom encoder settings"
    )

    # Flow options
    flowGroup = argParser.add_argument_group("Optical Flow")
    flowGroup.add_argument(
        "--flow", action="store_true", help="Extract the Optical Flow"
    )

    # Stabilizer Options
    stabilizerGroup = argParser.add_argument_group("Stabilizer")
    stabilizerGroup.add_argument(
        "--stabilize", action="store_true", help="Stabilize the video using VidStab"
    )

    # Miscellaneous options
    miscGroup = argParser.add_argument_group("Miscellaneous")
    miscGroup.add_argument("--buffer_limit", type=int, default=50, help="Buffer limit")
    miscGroup.add_argument(
        "--audio",
        action="store_true",
        help="Extract and merge audio track",
        default=True,
    )
    miscGroup.add_argument(
        "--benchmark", action="store_true", help="Benchmark the script"
    )
    miscGroup.add_argument(
        "--offline",
        type=str,
        nargs="*",
        default="none",
        help="Download a specific model or multiple models for offline use, use keyword 'all' to download all models",
    )
    miscGroup.add_argument(
        "--ae",
        action="store_true",
        help="Notify if script is run from After Effects interface",
    )
    miscGroup.add_argument(
        "--bit_depth",
        type=str,
        default="8bit",
        help="Bit Depth of the raw pipe input to FFMPEG. Useful if you want the highest quality possible - this doesn't have anything to do with --pix_fmt of the encoded ffmpeg.",
        choices=["8bit", "16bit"],
    )

    args = argParser.parse_args()
    return argumentsChecker(args, mainPath, outputPath)


def argumentsChecker(args, mainPath, outputPath):
    banner = r"""
__/\\\\\\\\\\\\\\\_____/\\\\\\\\\________/\\\\\\\\\\\___        
 _\///////\\\/////____/\\\\\\\\\\\\\____/\\\/////////\\\_       
  _______\/\\\________/\\\/////////\\\__\//\\\______\///__      
   _______\/\\\_______\/\\\_______\/\\\___\////\\\_________     
    _______\/\\\_______\/\\\\\\\\\\\\\\\______\////\\\______    
     _______\/\\\_______\/\\\/////////\\\_________\////\\\___   
      _______\/\\\_______\/\\\_______\/\\\__/\\\______\//\\\__  
       _______\/\\\_______\/\\\_______\/\\\_\///\\\\\\\\\\\/___ 
        _______\///________\///________\///____\///////////_____
"""

    if not args.benchmark and not args.hide_banner:
        print(red(banner))

    args.sharpen_sens /= 100
    args.autoclip_sens = 100 - args.autoclip_sens

    logging.info("============== Arguments ==============")

    argsDict = vars(args)
    for arg in argsDict:
        if argsDict[arg] is None or argsDict[arg] in ["", "none"] or argsDict[arg] is False:
            continue
        logging.info(f"{arg.upper()}: {argsDict[arg]}")
    
    checkSystem()

    logging.info("\n============== Arguments Checker ==============")
    args.ffmpeg_path = getFFMPEG()

    if args.offline != "none":
        toPrint = "Offline mode enabled, downloading all available models, this can take some time but it will allow for the script to be used offline"
        logging.info(toPrint)
        print(green(toPrint))

        options = modelsList() if args.offline == ["all"] else args.offline
        for option in options:
            for precision in [True, False]:
                try:
                    option = option.lower()
                    downloadModels(option, half=precision)
                except Exception as e:
                    logging.error(e)
                    print(
                        red(
                            f"Failed to download model: {option} with precision: "
                            + ("fp16" if precision else "fp32")
                        )
                    )

        toPrint = "All models downloaded!"
        logging.info(toPrint)
        print(green(toPrint))

    if args.dedup:
        logging.info("Dedup is enabled, audio will be disabled")
        args.audio = False

    if args.dedup_method in ["ssim", "ssim-cuda"]:
        args.dedup_sens = 1.0 - (args.dedup_sens / 1000)
        logging.info(
            f"New dedup sensitivity for {args.dedup_method} is: {args.dedup_sens}"
        )

    if args.scenechange_sens:
        if args.scenechange_method == [
            "differential",
            "differential-tensorrt",
            "diffrential-directml",
        ]:
            args.scenechange_sens = 0.65 - (args.scenechange_sens / 1000)
            logging.info(
                f"New scenechange sensitivity for {args.scenechange_method} is: {args.scenechange_sens}"
            )
        elif args.scenechange_method in [
            "shift_lpips",
            "shift_lpips-tensorrt",
            "shift_lpips-directml",
        ]:
            args.scenechange_sens = 0.50 - (args.scenechange_sens / 1000)
            logging.info(
                f"New scenechange sensitivity for {args.scenechange_method} is: {args.scenechange_sens}"
            )
        else:
            args.scenechange_sens = 0.9 - (args.scenechange_sens / 1000)
            logging.info(f"New scenechange sensitivity is: {args.scenechange_sens}")

    if args.custom_encoder:
        logging.info(
            "Custom encoder specified, use with caution since some functions can make or break the encoding process"
        )
    else:
        logging.info("No custom encoder specified, using default encoder")

    if args.upscale_skip:
        logging.info(
            "Upscale skip enabled, the script will skip frames that are upscaled to save time, this is far from perfect and can cause issues"
        )

    if args.upscale_skip and args.dedup:
        logging.error(
            "Upscale skip and dedup cannot be used together, disabling upscale skip to prevent issues"
        )
        args.upscale_skip = False

    if args.upscale_skip and not args.upscale:
        logging.error(
            "Upscale skip is enabled but upscaling is not, disabling upscale skip"
        )
        args.upscale_skip = False

    if args.bit_depth == "16bit" and args.segment:
        logging.error(
            "16bit input is not supported with segmentation, defaulting to 8bit"
        )
        args.bit_depth = "8bit"

    if args.encode_method in ["gif", "image"]:
        logging.info("GIF encoding selected, disabling audio")
        args.audio = False
        if args.preview:
            logging.error(
                "Preview is not supported with GIF and Image encoding, disabling preview"
            )
            args.preview = False

    if args.preview:
        logging.info(
            "Preview is enabled, the script will start a preview server to show the video during processing, this can have a signficant impact on performance"
        )
        print(
            green(
                "Preview is enabled, the script will start a preview server to show the video during processing, this can have a signficant impact on performance"
            )
        )

    args.isImage = False
    if args.input is None:
        toPrint = "No input specified, please specify an input file or URL to continue"
        logging.error(toPrint)
        print(red(toPrint))
        sys.exit()
    elif args.input.startswith("http") or args.input.startswith("www"):
            processURL(args, outputPath)

    elif args.input.endswith((".png", ".jpg", ".jpeg")):
        logging.info("Image input detected, disabling audio")
        args.audio = False
        if args.encode_method not in [".gif", "image"]:
            logging.error(
                "Image input detected but encoding method is not set to GIF or Image, defaulting to Image encoding"
            )
            args.encode_method = "image"
            args.isImage = True

    else:
        try:
            args.input = os.path.abspath(args.input)
            args.input = str(args.input)
        except Exception:
            logging.error(
                "Error processing the input, this is usually because of weird input names with spaces or characters that are not allowed"
            )
            sys.exit()

    processingMethods = [
        args.interpolate,
        args.scenechange,
        args.upscale,
        args.segment,
        args.denoise,
        args.sharpen,
        args.resize,
        args.dedup,
        args.depth,
        args.autoclip,
        args.flow,
        args.stabilize,
    ]

    if not any(processingMethods):
        toPrint = "No other processing methods specified, exiting"
        logging.error(toPrint)
        print(red(toPrint))
        sys.exit()

    return args


def processURL(args, outputPath):
    """
    Check if the input is a URL, if it is, download the video and set the input to the downloaded video
    """
    result = urlparse(args.input)
    if result.netloc.lower() in ["www.youtube.com", "youtube.com", "youtu.be"]:
        logging.info("URL is valid and will be used for processing")

        if args.output is None:
            outputFolder = os.path.join(outputPath, "output")
            os.makedirs(os.path.join(outputFolder), exist_ok=True)
            args.output = os.path.join(outputFolder, outputNameGenerator(args))

        VideoDownloader(
            args.input,
            args.output,
            args.encode_method,
            args.custom_encoder,
            args.ffmpeg_path,
            args.ae,
        )

        args.input = str(args.output)
        args.output = None
        logging.info(f"New input path: {args.input}")
    else:
        logging.error(
            "URL is invalid or not a YouTube URL, please check the URL and try again"
        )
        sys.exit()
