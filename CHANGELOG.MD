
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [UNRELEASED] - YYYY-MM-DD

### The Anime Scripter

##### NEW
- Added `Rife4.22-Lite` and `Rife4.22-Lite-Tensorrt`

##### Improvements
- Upgraded base polygraphy from 0.49.12 -> 0.49.13
- Removed unnecessary clamps.
- The metadata, progress bar and everything else related to video details should be MUCH more accurate now, including logging.
- Log.txt should now be more compact with `Arguments` no longer having unused arguments.
- Rife TRT will only build Static Engines in order to improve stability and versatility.
- Rife CUDA is now up to 10% faster than before.
- Benchmarks are now going to be more accurate for interpolation.
- Upgraded ONNXRuntime-DirectML to 1.19.1
- Improved the progress bar with more information and less unnecessary eye candy.
- Improved stability of image inputs.
- More video metadata requests.

#### Adobe Edition

#### NEW
- Added `Rife4.22-Lite` and `Rife4.22-Lite-Tensorrt` options to the dropdowns.

## [1.9.5] - 2024-08-17

### The Anime Scripter
N/A

### Adobe Edition

#### Fixes
- Fixed issues with `Full` or `Lite` Method selection in model download.

## [1.9.4] - 2024-08-17

### The Anime Scripter

#### New
- A new 3D like Banner :)
- Added OpenProteus and AniScale2 by Sirosky
- New lite version of TAS ( WIP )
- Support for multi audio and multi subtitle extraction and addition.
- Added ShuffleSpan by Sudo ( WIP )
- Added `Differential` | `Differential-TensorRT` ( My own attempts ) at a scenechange method ( WIP )
- Added `Shift_LPIPS-TensorRT` Scenechange Methods by Sudo.
- New `--hide_banner` flag to Hide TAS' banner when processing.
- Preview functionality with the command `--preview`, use port `127.0.0.1:5050/frame` in order to check the results of TAS.

#### Improvements
- Improved parameters and examples.
- Upgraded to nightly ONNXRuntime DirectML in order to avoid IR issues.
- Added recursive checks for Model Downloads.
- Significantly better I/O folder handling, this should result in better edge case handling.

#### Fixes
- Fixed a bug with 16bit workflow and x264_animation_10bit
- [Issue #44](https://github.com/NevermindNilas/TheAnimeScripter/issues/45)
- Fixes issues with input folder and output folder cases.
- [Issue #46](https://github.com/NevermindNilas/TheAnimeScripter/issues/46) - Fixed concurrency issues associated with Rife TensorRT and high cpu usages.
- Fixed an issues with span-directml where it would point to a different host.

#### Regressions
- Temporarely reverted back to pytorch 2.2.2 and cuda 12.1 until .dll issues are fixed, this may result in slight performance losses.

#### Removals
- Updater.exe

### Adobe Edition

#### New
- TAS will now dynamically switch between "Full" or "Lite" mode depending on your available GPU.

#### Improved
- Improved Error handling.
- The terminal ( command prompt ) will now start minimized in order to not disrupt your workflow.
- Immense improvements on output handling, TAS will now selectively create and choose specific types of folders based on your current process. This also comes with nice text formatting for the output with keywords like "_DE" for Deduplication and "_SH" for Sharpen.
- Better download functionality with a possibility in increased max download speed.

#### Bug Fixes
- For some users the download would often hang, this should now have been remedied or at least improved and TAS should now attempt to reconnect in case of a error connection.

## [1.9.3] - 2024-08-09

### The Anime Scripter

#### New
- Added Rife4.22 TensorRT
- Added Video Stabilization using Vidgear

#### Improvements

#### Removals

#### Fixed

### The Anime Scripter - Adobe Edition

#### New
- TBA

#### Improvements
- TBA


## [1.9.2] - 2024-08-09

### The Anime Scripter

#### New
- !Upgraded to Python 3.12!
- Rife 4.22 CUDA
- Rife 4.21 CUDA and TensorRT
- Rife 4.20 TensorRT
- Added `--bit_depth` in order to enable higher precision workflows. Options [8bit, 16bit].
- .GIF input support using `--encode_method gif` - STILL A WIP!!!
- .png / .jpeg support using `--encode_method image` - STILL A WIP!!!
- A complete overhaul on how model downloading works, it is recommended to go to Appdata\Roaming\TheAnimeScripter\Weights and deleting the whole folder with this version
- Released before 1.9.1 but wasn't announced, TAS now has nightly builds at: https://github.com/NevermindNilas/TAS-Nightly
- Upgraded SPAN Models to `2x_Spanimation V1.5` - Special thanks to @TNTWise for the models.

#### Improvements
- Up to 25% faster Rife TensorRT Inference performance.
- Better TensorRT Engine Handling in case if the engine / driver is outdated.
- Depth Maps should now produce significantly better outputs compared to previous releases at a roughly 5x deduction in performance.
- Made sure the output is now always clamped
- `--ofline` can now be dynamically selected to download a specific model or list of models based on user selection. Use keyword `all` to download all of the available models.
- The number of models have been drastically cut 
- TensorRT Engine workflow should now be drastically more robust than previously with better edge case handling.
- Revised documentation in Parameters.md
- Through a few 'optimizations' in model downloads, the total weights folder should be ~1.5GB lower.
- NCNN Upscaling models should now be dynamically downloaded based on user request
- Marginal performance boosts for Upscale NCNN
- Denoising is up to 2x faster now.
- Prebuilds will now be 100-150mb smaller.
- Audio Merging is now practically instantenous :)
- Compatability with vp9 and .webm processes
- Couple of changes to warplayer should have made it marginally faster and marginally more memory efficient.
- Decoding is now up to 15% faster.
- Deduplication is now up to 10% faster
- Sharpening is now up to 15% faster
- Benchmark will now use a selectable list for deciding the prefered GPU.

#### Removals:
- Rife4.15, Rife4.15-ncnn and Rife4.15-TensorRT

#### Fixes
- TensorRT artifactings when using Depth Maps.
- Depth Maps produced incostistent results with buggy and aliased outputs, TRT looked arguably worse than DirectML across the board.
- Scenechange Models have been renamed from " Maxvit " -> " Maxxvit " to better represent the real model.
- Fix issues with `--custom_encoder`
- Partial fix for issue [44](https://github.com/NevermindNilas/TheAnimeScripter/issues/44)
- TAS' ytdlp should now store the downloads in the output folder of main.exe in case if `--output` is not defined.
- Fixed some bugs / issues with Pathing for Linux.

#### The Anime Scripter - Adobe Edition

#### New
- Enabled auto clip functionality.
- Half-Automated TAS updates.
- `--bit_depth` has been added to the encoding settings.

#### Improvements
- More UI Changes.
- Simplified some backend functionality for better performance

#### Fixed
- Some weird scaling issues.
- TAS Update popping up randomly at times and closing.

## [1.9.1] - 2024-07-30
 
### The Anime Scripter

#### New
- Added Rife 4.20 CUDA.
- Added Depth Anything V2 - DirectML.
- New variable named `--scenechange_method` with choices `maxvit-directml` & `maxvit-tensorrt` ( special thanks to @sudo for the models ).
- ProRes 444 HQ Encoder ( `--encode_method prores` )
- Added Prores encoding support

#### Improvements
- Up to 15% faster Upscaling Performance when using TensorRT.
- Up to 20% faster Upscaling Performance when using CUDA.
- Up to 10% faster Interpolation Performance when using TensorRT.
- Up to 30% faster Interpolation Performance when using CUDA.
- Decoupled Scenechange from interpolation.
- Up to 20% faster SceneChange performance when using DirectML & TensorRT.
- Rife UHD Mode should allow for a bit more flexibility.
- Scenechange should no longer be reliant on the floating point precision of the interpolation process.
- More dynamic imports for faster startup times.
- Upgraded Torch version from 2.2.2 -> 2.4.0.
- Upgraded CUDA version from 12.1 -> 12.5.
- Reformated and cleaned up the code.
- `--help` should display a bit nicer now compared to previous releases and it should have more `helpers` added to them.
 
#### Fixed
- Issue [43](https://github.com/NevermindNilas/TheAnimeScripter/issues/43).
- Issue [41](https://github.com/NevermindNilas/TheAnimeScripter/issues/41).
- A couple of issues with scenechange caching.
- Fix issues with benchmark.py
- DLL missing with onnxruntime-directml

#### The Anime Scripter - Adobe Edition

#### New
- New installation method with code signing for a more secure and robust installation method.
- Dynamic Downloading and Updating of TAS.
- Pre-Render now works with more than 1 active / selected layer

#### Improvements
- A lot of UI Changes to streamline the look of TAS and make it more compact ( still a WIP )
- The `About` Page has been changed into a Help Icon on the left Bottom.
- More Tooltips and informations on everything that is going on.
- A progress bar for when you download a new release of TAS ( still a WIP )
- The 'executable' is now ONLY 230kb on initial launch and it will soon allow for a more broader usecase with both a "Full" and "Lite" version of TAS.
- The dropdowns now have proper hinting and sectioning of which model is for which gpu architechture.
- Added new Models and Encoders to the UI.
- Improved the performance and reduced some jankyness from the backend.
- Changed preset template from lossless to highquality to reduce overall space for rendering

#### Fixed
- Fixed a bug where inpoint / outpoint would go out of bounds.
- Fixed a bug where Youtube imports failed if no composition was selected.
- Fixed a bug where pre-render would not not adjust the work area properly before processing.
