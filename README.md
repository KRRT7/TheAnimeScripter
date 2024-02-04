<p align="center">
    <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FNevermindNilas%2FTheAnimeScripter%2F"><img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2FNevermindNilas%2FTheAnimeScripter%2F&labelColor=%23697689&countColor=%23ff8a65&style=plastic&labelStyle=none" /></a> 
    <a href="https://github.com/NevermindNilas/TheAnimeScripter/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/NevermindNilas/TheAnimeScripter.svg?style=flat-square" /></a>
    <a href="https://github.com/NevermindNilas/TheAnimeScripter/releases"><img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/NevermindNilas/TheAnimeScripter/total.svg?style=flat-square&color=%2364ff82" /></a>
    <a href="https://github.com/NevermindNilas/TheAnimeScripter/commits"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/NevermindNilas/TheAnimeScripter.svg?style=flat-square" /></a>
</p>
<p align="center">
    <a href="https://www.buymeacoffee.com/nilas" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>

# TheAnimeScripter

Welcome to TheAnimeScripter, a comprehensive tool designed for both video processing enthusiasts and professionals all within After Effects. Our tool offers a wide array of functionalities, including interpolation, upscaling, deduplication, segmentation, and more.

[Join The Discord Server](https://discord.gg/bFA6xZxM5V)

## Promo Video
[![Promo Video](https://img.youtube.com/vi/V7ryKMezqeQ/0.jpg)](https://youtu.be/V7ryKMezqeQ)



## 🚀 Key Features

1. **Smooth Motion Interpolation:** Elevate video quality with seamless frame interpolation for fluid motion.

2. **Crystal-Clear Upscaling:** Immerse audiences in enhanced resolution, delivering sharper, more detailed visuals.

3. **Optimal Video Size Deduplication:** Streamline videos by intelligently removing redundant frames, optimizing file size.

4. **Effortless Background-Foreground Segmentation:** Simplify rotobrushing tasks with precision and ease.

5. **3D Wizardry - Depth Map Generation:** Unlock advanced editing possibilities with detailed depth maps for immersive 3D effects.

6. **Auto Clip Cutting with Scene Change Filter:** Boost productivity by automatically cutting clips with a Scene Change Filter.

7. **Realistic Dynamics - Motion Blur:** Infuse realism into videos with customizable motion blur for a cinematic touch.

8. **Seamless After Effects Integration:** Enhance After Effects projects effortlessly with our seamless integration.

9. **Multi-Effect Magic - Model Chaining:** Combine features seamlessly within After Effects, running Deduplication, Upscaling, and Interpolation in one go.

10. **Efficient In-Memory Processing:** Experience swift transformations without additional frame extraction cycles.

11. **Custom Model Support for Creativity:** Unleash your creativity by incorporating your own trained models effortlessly.

Empower your video editing journey with these robust, efficient features designed to elevate your content to new heights.



## ✅ Stats
![Alt](https://repobeats.axiom.co/api/embed/4754b52201c8220b8611a8c6e43c53ed3dc82a9f.svg "Repobeats analytics image")

## 🛠️ Getting Started

#### How to download

- Download one of the latest releases from [here](https://github.com/NevermindNilas/TheAnimeScripter/releases)

#### Or Manually build

- **Notation needed, the code in the repository can include unexpected bugs, if you want stable builds then download from the releases page, but if you want the cutting edge builds, then follow along.**

- Download and install Python 3.12 from: https://www.python.org/downloads/release/python-3121/ whilst making sure to add it to System Path

- Open a terminal inside the folder

- run: ```python build.py```

#### How to use inside of After Effects

- On the top left corner open File -> Scripts -> Install ScriptUI Panel -> (Look for the TheAnimeScripter.jsx file found in folder )

- After Instalation you will be prompted with a restart of After Effects, do it.

- Now that you've reopened After Effects, go to Window -> And at the bottom of you should have a TheAnimeScripter.jsx, click it -> Dock the panel wherever you please.

- In the settings panel, set folder to the same directory as The Anime Scripter and output to wherever you please

## 📚 Available Inputs

- `--version` : (bool, action=store_true) Outputs the script version
- `--input` : (str) Absolute path of the input video.
- `--output` : (str) Output string of the video, can be absolute path or just a name.
- `--interpolate` : (int, default=0) Set to 1 if you want to enable interpolation, 0 to disable.
- `--interpolate_factor` : (int, default=2) Factor by which to interpolate.
- `--interpolate_method` : (str, default="rife") Method to use for interpolation. Options: "rife", "rife4.6", "rife4.14", "rife4.14-lite", "rife4.13-lite", "rife-ncnn", "rife4.6-ncnn", "rife4.14-ncnn", "rife4.14-lite-ncnn", "rife4.13-lite-ncnn"
- `--upscale` : (int, default=0) Set to 1 if you want to enable upscaling, 0 to disable.
- `--upscale_factor` : (int, default=2) Factor by which to upscale.
- `--upscale_method` : (str, default="ShuffleCugan") Method to use for upscaling. Options: "cugan / cugan-ncnn / shufflecugan ", "swinir", "compact / ultracompact / superultracompact", "span", "omnisr"
- `--cugan_kind` : (str, default="no-denoise") Kind of Cugan to use. Options: "no-denoise", "conservative", "denoise1x", "denoise2x"
- `--dedup` : (int, default=0) Set to 1 if you want to enable deduplication, 0 to disable.
- `--dedup_method` : (str, default="ffmpeg") Method to use for deduplication.
- `--dedup_sens` : (float, default=50) Sensitivy of deduplication.
- `--half` : (int, default=1) Set to 1 to use half precision, 0 for full precision.
- `--inpoint` : (float, default=0) Inpoint for the video.
- `--outpoint` : (float, default=0) Outpoint for the video.
- `--sharpen` : (int, default=0) Set to 1 if you want to enable sharpening, 0 to disable.
- `--sharpen_sens` : (float, default=50) Sensitivity of sharpening.
- `--segment` : (int, default=0) Set to 1 if you want to enable segmentation, 0 to disable.
- `--scenechange` : (int, default=0) Set to 1 if you want to enable scene change detection, 0 to disable.
- `--scenechange_sens` : (float, default=40) Sensitivity of scene change detection.
- `--depth` : (int, default=0) Generate Depth Maps, 1 to enable, 0 to disable
- `--depth_method` : (str, default="small") Choose which model to utilize, can be small, base, large
- `--encode_method` : (str, default="x264") Method to use for encoding. Options: x264, x264_animation, nvenc_h264, nvenc_h265, qsv_h264, qsv_h265, h264_amf, hevc_amf
- `--motion_blur` : (int, default=0) Add motion blur using gaussian weighting between multiple frames, relies on interpolate factor and method
- `--ytdlp` : (str, default="") Download a youtube video, needs full url.
- `--ytdlp_quality` : (int, default = 0) Allow 4k/8k videos to be downloaded then reencoded to selected `--encode_method`
- `--ensemble` : (int, default = 0) Activate Ensemble for higher quality outputs from Rife ( doesn't work with ncnn versions for now )
- `--resize` : (int, choices=[0, 1], default=0) Set to 1 if you want to enable resizing, 0 to disable. An alternative method to use for upscaling, specifically targetting lower end GPUs.
- `--resize_factor` : (int, default=2) Factor by which to resize the decoded video. Can also be a float value in between 0 and 1 for downscaling. The resizing will always try to maintain the original aspect ratio
- `--resize_method` : (str, choices=["fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos", "spline"], default="bicubic") "lanczos" is recommended for upscaling and "area" for downscaling.
- `--custom_model` :(str, default = "") Choose a different model for the supported upscaling arches. It relies on `--upscaling_factor` and `--upscaling_method`. The input must be a full path to a desired .pth or .onnx file.

## 🙏 Acknowledgements

- [SUDO](https://github.com/styler00dollar/VSGAN-tensorrt-docker) - For helping me debug my code and shufflecugan model
- [HZWER](https://github.com/hzwer/Practical-RIFE) - For Rife.
- [AILAB](https://github.com/bilibili/ailab/tree/main/Real-CUGAN) - For Cugan.
- [JingyunLiang](https://github.com/JingyunLiang/SwinIR) - For SwinIR.
- [Xintao](https://github.com/xinntao/Real-ESRGAN) - for Realesrgan, specifically compact arch.
- [the-database](https://github.com/the-database/mpv-upscale-2x_animejanai) - For Compact, UltraCompact, SuperUltraCompact models
- [Tohrusky](https://github.com/Tohrusky/realcugan-ncnn-py) - For RealCugan-NCNN-Vulkan wrapper.
- [SkyTNT](https://github.com/SkyTNT/anime-segmentation) - For Anime Segmentation.
- [LiheYoung](https://github.com/LiheYoung/Depth-Anything) - For Depth Anything.
- [98mxr](https://github.com/98mxr/GMFSS_Fortuna) - For GMFSS Fortuna Union.
- [HolyWU](https://github.com/HolyWu/vs-gmfss_fortuna/tree/master) - For VS GMFSS code.
- [FFmpeg Group](https://github.com/FFmpeg/FFmpeg) - For FFmpeg
- [Nihui](https://github.com/nihui/rife-ncnn-vulkan) - For Rife NCNN
- [Media2x](https://github.com/media2x/rife-ncnn-vulkan-python) - For Rife NCNN Wrapper
- [TNTWise](https://github.com/TNTwise/rife-ncnn-vulkan) - For newest implementations of Rife
- [YT-DLP](https://github.com/yt-dlp/yt-dlp) - For YT-DLP
- [Hongyuanyu](https://github.com/hongyuanyu/span) - For SPAN
- [Phhofm](https://github.com/phhofm) - For SwinIR, Span and OmniSR Models
- [Francis0625](https://github.com/Francis0625/Omni-SR) - For OmniSR

## 📈 Benchmarks

The following benchmarks were conducted on a system with a 13700k and 3090 GPU for 1920x1080p inputs and take x264 encoding into account, FP16 on where possible.

| Test Category | Method | FPS | Notes |
| --- | --- | --- | --- |
| **Interpolation 2x** |
| | Rife (v4.13-lite) | ~120 | Ensemble False |
| | Rife (v4.14-lite) | ~100 | Ensemble False |
| | Rife (v4.14) | ~100 | Ensemble False |
| | Rife (v4.13-lite) | ~100 | Ensemble True |
| | Rife (v4.14-lite) | ~80 | Ensemble True |
| | Rife (v4.14) | ~80 | Ensemble True |
| | Rife (v4.13-lite-ncnn) | ~60 |  |
| | Rife (v4.14-lite-ncnn) | ~50 |  |
| | Rife (v4.14-ncnn) | ~50 |  |
| | GMFSS Fortuna Union | ~7 | Ensemble False |
| **Upscaling 2x** | 
| | Shufflecugan | ~21 | |
| | Compact | ~15 | |
| | UltraCompact | ~25 | |
| | SuperUltraCompact | ~30 | |
| | SwinIR | ~1 | |
| | Cugan | ~9 | |
| | Cugan-NCNN | ~7 | |
| | SPAN | ~9 | |
| | OmniSR | ~1 | |
| **Depth Map Generation** | 
| | Depth Anything VITS | ~16 | |
| | Depth Anything VITB | ~11 | |
| | Depth Anything VITL | ~7 | |
| **Segmentation** | 
| | Isnet-Anime | ~10 | |
| **Motion Blur** | 
| | 2xRife + Gaussian Averaging | ~23 | Still in work |

Please note that these benchmarks are approximate and actual performance may vary based on specific video content, settings, and other factors.
