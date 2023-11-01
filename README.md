# Build for android libvips

This packaging script is only tested in the following environments:

1. macOS
2. NDK 25
3. conan 2.0.14
4. python 3.11.6

## Setup

- Install conan

```bash
pip install conan
```

- Add ANDROID_NDK to environment variables

```bash
export ANDROID_NDK=/path/to/ndk
```

- run the script

```bash
python build_android.py
python3 build_android.py

chmod +x build_android.py
./build_android.py
```
