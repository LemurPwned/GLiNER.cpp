
# GLiNER.cpp: Generalist and Lightweight Named Entity Recognition for C++ with Python bindings

Forked from: https://github.com/Knowledgator/GLiNER.cpp --> see there for the original repo


GLiNER.cpp is a C++-based inference engine for running GLiNER (Generalist and Lightweight Named Entity Recognition) models. GLiNER can identify any entity type using a bidirectional transformer encoder, offering a practical alternative to traditional NER models and large language models.

## TlDr;

```bash
# clone the repo 
cd GLiNER.cpp && python -m pip install .
```

## WebAssembly bindings

The project can also be built with Emscripten to obtain a WebAssembly module that exposes the same inference API for browser applications (for example, React).

1. Install the [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html) and activate it (`source /path/to/emsdk_env.sh`).
2. Build ONNX Runtime for the wasm target and point `ONNXRUNTIME_ROOTDIR` to the unpacked SDK that contains `libonnxruntime_webassembly.a` together with the headers. Native prebuilt downloads are not compatible with the wasm build.
3. Configure and build using the Emscripten tooling:

```bash
emcmake cmake -B build-wasm -S . \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_WASM=ON \
  -DONNXRUNTIME_ROOTDIR=/absolute/path/to/onnxruntime-wasm
emmake cmake --build build-wasm -j
```

The generated module lives under `build-wasm/bindings/` (for example `gliner.js` and `gliner.wasm`) and is emitted with `MODULARIZE=1` and ES module output:

```javascript
import createGLiNER from './gliner.js';

const Module = await createGLiNER();
Module.FS.writeFile('model.onnx', modelBytes);
Module.FS.writeFile('tokenizer.json', tokenizerBytes);

const cfg = Module.createConfig(12, 512, Module.ModelType.SPAN_LEVEL);
const model = new Module.Model('model.onnx', 'tokenizer.json', cfg);
const spans = model.inference(['The capital of France is Paris.'], ['LOCATION']);
```

Use the embedded `FS` helper to stage model/tokenizer assets before constructing the model. If your ONNX Runtime wasm build splits functionality into multiple static libraries, pass them with `-DONNXRUNTIME_EXTRA_LIBS="libonnxruntime_providers.a;libonnxruntime_common.a"` during configuration.

## Example 

ONNX model example

```python
import gliner_cpp
import time

cfg = gliner_cpp.Config(12, 512)
MODEL_PATH = "./models/model.onnx"
TOKENIZER_PATH = "./models/tokenizer.json"
start = time.time()
model = gliner_cpp.Model(MODEL_PATH, TOKENIZER_PATH, cfg)
end = time.time()
print(f"Loading model took: {end - start} seconds")


test = "The capital of France is Paris. I visited last in September last year."
entities = ["LOCATION", "COUNTRY", "DATE"]
start = time.time()
spans = model.inference([test], entities)
for span in spans:
    print(span)
end = time.time()
print(f"Inference took: {end - start} seconds")

```
