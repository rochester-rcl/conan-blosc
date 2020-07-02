### Conan Recipe for [Blosc](https://github.com/Blosc/c-blosc)

#### To Build Library

```bash
./build.sh
```

Or

```bash
conan source . -sf src 
conan install . -if build --build missing
conan build . -bf build -sf src
conan export-pkg . Blosc/1.5.0@rcldsl/stable -s build_type=Release -sf src -bf build
```
