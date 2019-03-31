# Demo project to compile Crate dependencies with Meson

This project builds a Rust program that uses a few simple crates from
crates.io. The crates are downloaded using the crates.io REST API, and are
converted to build with meson instead of Cargo.

Check `meson.build` to see which crates are used.

To run it do the following:

```shell
mkdir subprojects # This is where the crates end up
meson build
ninja -C build
build/prog
```

Running the final program should give you the following output:

```shell
Converted number: [49, 50, 56]
```
