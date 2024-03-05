import subprocess
import os
import shutil
from importlib.metadata import distribution

base_dir = os.path.dirname(os.path.abspath(__file__))


def create_venv():
    print("Creating the virtual environment...")
    subprocess.run(["python", "-m", "venv", "venv"], check=True)


def activate_venv():
    print("Activating the virtual environment...")
    subprocess.run(".\\venv\\Scripts\\activate", shell=True, check=True)


def install_requirements():
    print("Installing the requirements...")
    subprocess.run(
        [".\\venv\\Scripts\\pip3", "install", "-r", "requirements.txt"],
        check=True,
    )


def install_pyinstaller():
    print("Installing PyInstaller...")
    subprocess.run(
        [".\\venv\\Scripts\\python", "-m", "pip", "install", "pyinstaller"], check=True
    )


def create_executable():
    print("Creating executable with PyInstaller...")
    src_path = os.path.join(base_dir, "src")
    main_path = os.path.join(base_dir, "main.py")
    icon_path = os.path.join(base_dir, "demos", "icon.ico")
    cugan_ncnn_models_path = os.path.join(
        distribution("realcugan_ncnn_py").locate_file("realcugan_ncnn_py"),
        "models",
    )
    rife_ncnn_models_path = os.path.join(
        distribution("rife_ncnn_vulkan_python").locate_file("rife_ncnn_vulkan_python"),
        "models",
    )
    span_ncnn_models_path = os.path.join(
        distribution("span_ncnn_py").locate_file("span_ncnn_py"),
        "models",
    )
    realesrgan_ncnn_models_path = os.path.join(
        distribution("realesrgan_ncnn_py").locate_file("realesrgan_ncnn_py"),
        "models",
    )

    subprocess.run(
        [
            ".\\venv\\Scripts\\pyinstaller",
            "--noconfirm",
            "--onedir",
            "--console",
            "--noupx",
            "--clean",
            "--add-data",
            f"{src_path};src/",
            "--add-data",
            f"{cugan_ncnn_models_path};realcugan_ncnn_py/models",
            "--add-data",
            f"{rife_ncnn_models_path};rife_ncnn_vulkan_python/models",
            "--add-data",
            f"{span_ncnn_models_path};span_ncnn_py/models",
            "--add-data",
            f"{realesrgan_ncnn_models_path};realesrgan_ncnn_py/models",
            "--hidden-import",
            "realcugan_ncnn_py.realcugan_ncnn_wrapper",
            "--hidden-import",
            "span_ncnn_py.span_ncnn_wrapper",
            "--hidden-import",
            "rife_ncnn_vulkan_python.rife_ncnn_vulkan_wrapper",
            "--hidden-import",
            "realesrgan_ncnn_py.realesrgan_ncnn_py_wrapper",
            "--collect-all",
            "cupy",
            "--collect-all",
            "cupyx",
            "--collect-all",
            "cupy_backends",
            "--collect-all",
            "fastrlock",
            "--icon",
            f"{icon_path}",
            main_path,
        ],
        check=True,
    )


def move_extras():
    dist_dir = os.path.join(base_dir, "dist")
    main_dir = os.path.join(dist_dir, "main")
    jsx_path = os.path.join(base_dir, "TheAnimeScripter.jsx")
    license_path = os.path.join(base_dir, "LICENSE")
    readme_path = os.path.join(base_dir, "README.md")
    readme_txt_path = os.path.join(base_dir, "README.txt")
    target_path = os.path.join(main_dir, os.path.basename(jsx_path))
    try:
        shutil.copy(jsx_path, target_path)
        shutil.copy(license_path, main_dir)
        shutil.copy(readme_path, main_dir)
        shutil.copy(readme_txt_path, main_dir)
    except Exception as e:
        print("Error while copying jsx file: ", e)


def clean_up():
    # Seems like pyinstaller duplicates some dll files due to cupy cuda
    # Removing them in order to fit the <2GB limit
    dllFiles = [
        "cublasLt64_12.dll",
        "cusparse64_12.dll",
        "cufft64_11.dll",
        "cusolver64_11.dll",
        "cublas64_12.dll",
        "curand64_10.dll",
        "nvrtc64_120_0.dll",
        "nvJitLink_120_0.dll"
    ]
    dllPath = os.path.join(base_dir, "dist", "main", "_internal")

    for file in dllFiles:
        try:
            os.remove(os.path.join(dllPath, file))
        except Exception as e:
            print("Error while removing dll file: ", e)

    print("\n")
    answer = input("Do you want to clean up the residual files? (y/n): ")

    if answer.lower() == "y":
        print("Cleaning up...")
        try:
            spec_file = os.path.join(base_dir, "main.spec")
            if os.path.exists(spec_file):
                os.remove(spec_file)
        except Exception as e:
            print("Error while removing spec file: ", e)

        try:
            venv_file = os.path.join(base_dir, "venv")
            if os.path.exists(venv_file):
                shutil.rmtree(venv_file)
        except Exception as e:
            print("Error while removing the venv: ", e)

        try:
            build_dir = os.path.join(base_dir, "build")
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
        except Exception as e:
            print("Error while removing the build directory: ", e)
    else:
        print("Skipping Cleanup...")

    print("Done!, you can find the built executable in the dist folder")


if __name__ == "__main__":
    create_venv()
    activate_venv()
    install_requirements()
    install_pyinstaller()
    create_executable()
    move_extras()
    clean_up()
