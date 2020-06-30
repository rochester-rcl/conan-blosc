#!/bin/bash
mkdir src 
mkdir build
conan source . -sf src 
conan install . -if build --build
conan build . -bf build -sf src
conan export-pkg . Blosc/1.5.0@rcldsl/stable -s build_type=Release -sf src -bf build --force