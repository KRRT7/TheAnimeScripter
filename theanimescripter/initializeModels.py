import logging


def AutoClip(self, mainPath):
    from theanimescripter.autoclip.autoclip import AutoClip

    AutoClip(
        self.input,
        self.autoclip_sens,
        mainPath,
        self.inpoint,
        self.outpoint,
    )


def Segment(self):
    # Lazy loading for startup time reasons

    if self.segment_method == "anime":
        from theanimescripter.segment.animeSegment import AnimeSegment

        AnimeSegment(
            self.input,
            self.output,
            self.ffmpeg_path,
            self.width,
            self.height,
            self.outputFPS,
            self.inpoint,
            self.outpoint,
            self.encode_method,
            self.custom_encoder,
            self.buffer_limit,
            self.benchmark,
            self.totalFrames,
        )
    elif self.segment_method == "anime-tensorrt":
        from theanimescripter.segment.animeSegment import AnimeSegmentTensorRT

        AnimeSegmentTensorRT(
            self.input,
            self.output,
            self.ffmpeg_path,
            self.width,
            self.height,
            self.outputFPS,
            self.inpoint,
            self.outpoint,
            self.encode_method,
            self.custom_encoder,
            self.buffer_limit,
            self.benchmark,
            self.totalFrames,
        )

    elif self.segment_method == "anime-directml":
        from theanimescripter.segment.animeSegment import AnimeSegmentDirectML

        AnimeSegmentDirectML(
            self.input,
            self.output,
            self.ffmpeg_path,
            self.width,
            self.height,
            self.outputFPS,
            self.inpoint,
            self.outpoint,
            self.encode_method,
            self.custom_encoder,
            self.buffer_limit,
            self.benchmark,
            self.totalFrames,
        )


def Depth(self):
    match self.depth_method:
        case "small_v2" | "base_v2" | "large_v2":
            from theanimescripter.depth.depth import DepthV2

            DepthV2(
                self.input,
                self.output,
                self.ffmpeg_path,
                self.width,
                self.height,
                self.fps,
                self.half,
                self.inpoint,
                self.outpoint,
                self.encode_method,
                self.depth_method,
                self.custom_encoder,
                self.buffer_limit,
                self.benchmark,
                self.totalFrames,
                self.bit_depth,
            )

        case "small_v2-tensorrt" | "base_v2-tensorrt" | "large_v2-tensorrt":
            from theanimescripter.depth.depth import DepthTensorRTV2

            DepthTensorRTV2(
                self.input,
                self.output,
                self.ffmpeg_path,
                self.width,
                self.height,
                self.fps,
                self.half,
                self.inpoint,
                self.outpoint,
                self.encode_method,
                self.depth_method,
                self.custom_encoder,
                self.buffer_limit,
                self.benchmark,
                self.totalFrames,
                self.bit_depth,
            )

        case "small_v2-directml" | "base_v2-directml" | "large_v2-directml":
            from theanimescripter.depth.depth import DepthDirectMLV2

            DepthDirectMLV2(
                self.input,
                self.output,
                self.ffmpeg_path,
                self.width,
                self.height,
                self.fps,
                self.half,
                self.inpoint,
                self.outpoint,
                self.encode_method,
                self.depth_method,
                self.custom_encoder,
                self.buffer_limit,
                self.benchmark,
                self.totalFrames,
                self.bit_depth,
            )


def Stabilize(self):
    from theanimescripter.stabilize.stabilize import VideoStabilizer

    VideoStabilizer(
        self.input,
        self.output,
        self.ffmpeg_path,
        self.width,
        self.height,
        self.fps,
        self.half,
        self.inpoint,
        self.outpoint,
        self.encode_method,
        self.custom_encoder,
        self.buffer_limit,
        self.benchmark,
        self.totalFrames,
    )


def initializeModels(self):
    outputWidth = self.width
    outputHeight = self.height
    upscale_process = None
    interpolate_process = None
    denoise_process = None
    dedup_process = None
    scenechange_process = None
    upscaleSkipProcess = None

    if self.upscale:
        if self.upscale_skip:
            from theanimescripter.dedup.dedup import DedupSSIM

            upscaleSkipProcess = DedupSSIM(
                0.995,
            )

        from theanimescripter.unifiedUpscale import UniversalPytorch

        outputWidth *= self.upscale_factor
        outputHeight *= self.upscale_factor
        logging.info(f"Upscaling to {outputWidth}x{outputHeight}")
        match self.upscale_method:
            case (
                "shufflecugan"
                | "compact"
                | "ultracompact"
                | "superultracompact"
                | "span"
                | "open-proteus"
                | "aniscale2"
                | "shufflespan"
            ):
                upscale_process = UniversalPytorch(
                    self.upscale_method,
                    self.upscale_factor,
                    self.half,
                    self.width,
                    self.height,
                    self.custom_model,
                    upscaleSkipProcess,
                )

            case (
                "compact-directml"
                | "ultracompact-directml"
                | "superultracompact-directml"
                | "span-directml"
                | "shufflecugan-directml"
                | "open-proteus-directml"
                | "aniscale2-directml"
                | "shufflespan-directml"
            ):
                from theanimescripter.unifiedUpscale import UniversalDirectML

                upscale_process = UniversalDirectML(
                    self.upscale_method,
                    self.upscale_factor,
                    self.half,
                    self.width,
                    self.height,
                    self.custom_model,
                    upscaleSkipProcess,
                )

            case "shufflecugan-ncnn" | "span-ncnn":
                from theanimescripter.unifiedUpscale import UniversalNCNN

                upscale_process = UniversalNCNN(
                    self.upscale_method,
                    self.upscale_factor,
                    upscaleSkipProcess,
                )

            case (
                "shufflecugan-tensorrt"
                | "compact-tensorrt"
                | "ultracompact-tensorrt"
                | "superultracompact-tensorrt"
                | "span-tensorrt"
                | "open-proteus-tensorrt"
                | "aniscale2-tensorrt"
                | "shufflespan-tensorrt"
            ):
                from theanimescripter.unifiedUpscale import UniversalTensorRT

                upscale_process = UniversalTensorRT(
                    self.upscale_method,
                    self.upscale_factor,
                    self.half,
                    self.width,
                    self.height,
                    self.custom_model,
                    upscaleSkipProcess,
                )
    if self.interpolate:
        logging.info(
            f"Interpolating from {format(self.fps, '.3f')}fps to {format(self.fps * self.interpolate_factor, '.3f')}fps"
        )

        match self.interpolate_method:
            case (
                "rife"
                | "rife4.6"
                | "rife4.15-lite"
                | "rife4.16-lite"
                | "rife4.17"
                | "rife4.18"
                | "rife4.20"
                | "rife4.21"
                | "rife4.22"
                | "rife4.22-lite"
            ):
                from theanimescripter.unifiedInterpolate import RifeCuda

                interpolate_process = RifeCuda(
                    self.half,
                    outputWidth,
                    outputHeight,
                    self.interpolate_method,
                    self.ensemble,
                    self.interpolate_factor,
                    self.fps,
                )

            case (
                "rife-ncnn"
                | "rife4.6-ncnn"
                | "rife4.15-lite-ncnn"
                | "rife4.16-lite-ncnn"
                | "rife4.17-ncnn"
                | "rife4.18-ncnn"
            ):
                from theanimescripter.unifiedInterpolate import RifeNCNN

                interpolate_process = RifeNCNN(
                    self.interpolate_method,
                    self.ensemble,
                    outputWidth,
                    outputHeight,
                    self.half,
                )

            case (
                "rife-tensorrt"
                | "rife4.6-tensorrt"
                | "rife4.15-lite-tensorrt"
                | "rife4.17-tensorrt"
                | "rife4.18-tensorrt"
                | "rife4.20-tensorrt"
                | "rife4.21-tensorrt"
                | "rife4.22-tensorrt"
                | "rife4.22-lite-tensorrt"
            ):
                from theanimescripter.unifiedInterpolate import RifeTensorRT

                interpolate_process = RifeTensorRT(
                    self.interpolate_method,
                    self.interpolate_factor,
                    outputWidth,
                    outputHeight,
                    self.half,
                    self.ensemble,
                )

    if self.denoise:
        match self.denoise_method:
            case "scunet" | "dpir" | "nafnet" | "real-plksr":
                from theanimescripter.unifiedDenoise import UnifiedDenoise

                denoise_process = UnifiedDenoise(
                    self.denoise_method,
                    self.half,
                )

    if self.dedup:
        match self.dedup_method:
            case "ssim":
                from theanimescripter.dedup.dedup import DedupSSIM

                dedup_process = DedupSSIM(
                    self.dedup_sens,
                    self.sample_size,
                )

            case "mse":
                from theanimescripter.dedup.dedup import DedupMSE

                dedup_process = DedupMSE(
                    self.dedup_sens,
                    self.sample_size,
                )

            case "ssim-cuda":
                from theanimescripter.dedup.dedup import DedupSSIMCuda

                dedup_process = DedupSSIMCuda(
                    self.dedup_sens,
                    self.sample_size,
                    self.half,
                )

            case "mse-cuda":
                from theanimescripter.dedup.dedup import DedupMSECuda

                dedup_process = DedupMSECuda(
                    self.dedup_sens,
                    self.sample_size,
                    self.half,
                )

    if self.scenechange:
        match self.scenechange_method:
            case "maxxvit-tensorrt" | "shift_lpips-tensorrt":
                from theanimescripter.scenechange import SceneChangeTensorRT
                scenechange_process = SceneChangeTensorRT(
                    self.half,
                    self.scenechange_sens,
                    self.scenechange_method,
                )
            case "maxxvit-directml":
                from theanimescripter.scenechange import SceneChange

                scenechange_process = SceneChange(
                    self.half,
                    self.scenechange_sens,
                )
            case "differential":
                from theanimescripter.scenechange import SceneChangeCPU

                scenechange_process = SceneChangeCPU(
                    self.scenechange_sens,
                )
            case "differential-cuda":
                from theanimescripter.scenechange import SceneChangeCuda

                scenechange_process = SceneChangeCuda(
                    self.scenechange_sens,
                )
            case "differential-tensorrt":
                from theanimescripter.scenechange import DifferentialTensorRT

                scenechange_process = DifferentialTensorRT(
                    self.scenechange_sens,
                    self.height,
                    self.width,
                )
            case "differential-directml":
                # from theanimescripter.scenechange import DifferentialDirectML
                # scenechange_process = DifferentialDirectML(
                #     self.scenechange_sens,
                # )
                raise NotImplementedError(
                    "Differential DirectML is not implemented yet"
                )
            case _:
                raise ValueError(
                    f"Unknown scenechange method: {self.scenechange_method}"
                )

    return (
        outputWidth,
        outputHeight,
        upscale_process,
        interpolate_process,
        denoise_process,
        dedup_process,
        scenechange_process,
    )
