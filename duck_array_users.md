# Downstream use of pint's duck-array support

Which tested projects put something other than a plain NumPy array or scalar inside a pint `Quantity`, or run pint conversions directly on such arrays. Researched 2026-11-01 against each project's default branch, or the tag the tester pins where noted.

"Tester" says whether our `projects.toml` setup actually runs that code: right test path, and the array library installed in CI. CI installs were checked from run [40304567057](https://github.com/andrewgsavage/pint_downstream_tester/actions/runs/40304567057).

## By project

| Project | Array types | How | Evidence | Tester |
|---|---|---|---|---|
| [pint-xarray](https://github.com/xarray-contrib/pint-xarray) | xarray data: NumPy or **dask** | `.pint.quantify()` wraps DataArray data in Quantities; a unit-aware `.pint.chunk()` | [`accessors.py` L594](https://github.com/xarray-contrib/pint-xarray/blob/main/pint_xarray/accessors.py#L594), [`tests/test_accessors.py` L1177](https://github.com/xarray-contrib/pint-xarray/blob/main/pint_xarray/tests/test_accessors.py#L1177) (`@requires_dask_array`) | ✅ dask is in `test_deps` |
| [pint-pandas](https://github.com/hgrecco/pint-pandas) | **pandas ExtensionArrays** (`FloatingArray`, `IntegerArray`, `NumpyExtensionArray`), **`pd.NA`** | `PintArray._data` is an ExtensionArray, and Quantities are built from it and its elements | [`pint_array.py` L339, L465, L498](https://github.com/hgrecco/pint-pandas/blob/master/pint_pandas/pint_array.py#L339) | ✅ (76 tests broke on #2523) |
| [MetPy](https://github.com/Unidata/MetPy) | **dask**, **NumPy masked arrays** | The calc tests run every function with an `array_type` fixture: dask, masked, xarray or NumPy. `units.masked_array()`; the xarray accessor wraps `.data` (dask stays lazy) | [`conftest.py` L148–157 @v1.7.1](https://github.com/Unidata/MetPy/blob/v1.7.1/conftest.py#L148), [`units.py` L189–215](https://github.com/Unidata/MetPy/blob/main/src/metpy/units.py#L189), [`xarray.py` L165](https://github.com/Unidata/MetPy/blob/main/src/metpy/xarray.py#L165) | ⚠️ masked: yes. **dask: no**, because dask is only in MetPy's `extras` extra, so CI doesn't install it and the dask variants skip |
| [pairinteraction](https://github.com/pairinteraction/pairinteraction) | **`scipy.sparse.csr_matrix`** | Sparse Hamiltonian and operator matrices stored as Quantities (`PintSparse`) | [`units.py` L12, L27, L152](https://github.com/pairinteraction/pairinteraction/blob/master/src/pairinteraction/units.py#L12) | ✅ (69 tests broke on #2523) |
| [dinosaur](https://github.com/neuralgcm/dinosaur) | **JAX arrays** | `dimensionalize()` multiplies a `jnp` array by a Quantity; tests build `jnp.arange(77) * units.J / units.m**2` | [`scales.py` L30, L190–202](https://github.com/neuralgcm/dinosaur/blob/main/dinosaur/scales.py#L190), [`scales_test.py` L42](https://github.com/neuralgcm/dinosaur/blob/main/dinosaur/scales_test.py#L42) | ✅ jax is a dependency |
| [jpu](https://github.com/dfm/jpu) | **JAX arrays** | `JpuQuantity` subclasses pint's Quantity with `jnp` magnitudes | [`quantity.py` L60–82](https://github.com/dfm/jpu/blob/main/src/jpu/quantity.py#L60), `tests/test_numpy.py` | ✅ |
| [spectrochempy](https://github.com/spectrochempy/spectrochempy) | **NumPy masked arrays** | `NDDataset.values` returns `Quantity(np.ma.masked_where(...), units)` for masked data | [`ndarray.py` L1172–1189, L2310–2315](https://github.com/spectrochempy/spectrochempy/blob/master/src/spectrochempy/core/dataset/basearrays/ndarray.py#L2310) | ✅ |
| [xclim](https://github.com/Ouranosinc/xclim) | **dask** (via xarray `.data`) | Doesn't wrap arrays; calls `units.convert(source.data, src, tgt)` on the raw NumPy or dask data | [`core/units.py` ~L461](https://github.com/Ouranosinc/xclim/blob/main/src/xclim/core/units.py), [`tests/test_units.py` L87–89](https://github.com/Ouranosinc/xclim/blob/main/tests/test_units.py#L87) (asserts the result is still `dask.Array`) | ✅ dask is a dependency |
| [icclim](https://github.com/cerfacs-globc/icclim) | **dask** (indirect) | Converts through xclim's `convert_units_to` | [`indicator.py` L286–297](https://github.com/cerfacs-globc/icclim/blob/master/src/icclim/_core/generic/indicator.py#L286) | ✅ indirectly |
| [satpy](https://github.com/pytroll/satpy) | **dask** (xarray-backed) | Writers convert units with `dataset.pint.quantify().pint.to(units).pint.dequantify()` on dask DataArrays | [`writers/core/image.py` L105–106](https://github.com/pytroll/satpy/blob/main/satpy/writers/core/image.py#L105), [`writers/mitiff.py` L86–87](https://github.com/pytroll/satpy/blob/main/satpy/writers/mitiff.py#L86) | ✅ probably: CI installs pint-xarray via `satpy[tests]`, and the ninjogeotiff writer tests pass `units=` (not checked test by test) |
| [xMIP](https://github.com/jbusecke/xMIP) | xarray data (dask in real CMIP use) | `correct_units()` converts with `ds.pint.quantify()` / `.pint.to()` | [`preprocessing.py` L217–231](https://github.com/jbusecke/xMIP/blob/main/xmip/preprocessing.py#L217) | ✅ `test_correct_units` runs, but on NumPy-backed data |
| [cf-xarray](https://github.com/xarray-contrib/cf-xarray) | xarray data | Tests `.pint.quantify()` together with the cf accessor | [`tests/test_accessor.py` L266–270](https://github.com/xarray-contrib/cf-xarray/blob/main/cf_xarray/tests/test_accessor.py#L266) | ❌ pint-xarray isn't installed, so the test skips |
| [typhon](https://github.com/atmtools/typhon) | **NumPy masked arrays** | The TOVS readers build `ureg.Quantity(numpy.ma.MaskedArray(...))` | [`datasets/tovs.py` L439](https://github.com/atmtools/typhon/blob/master/typhon/datasets/tovs.py#L439) | ❌ probably not: those readers need data files |
| [DeepTrack2](https://github.com/DeepTrackAI/DeepTrack2) | **PyTorch tensors** | `ConversionTable.convert()` multiplies tensors by units, giving Quantities; tensors with `requires_grad` deliberately bypass pint | [`backend/units.py` L94–97, L389–418](https://github.com/DeepTrackAI/DeepTrack2/blob/develop/deeptrack/backend/units.py#L389) | ❌ torch isn't installed in CI, so only NumPy paths run |

Outside the 103 projects: **xarray** itself tests pint Quantities as a duck array inside DataArrays, including dask-chunked ones ([`xarray/tests/test_units.py`](https://github.com/pydata/xarray/blob/main/xarray/tests/test_units.py)). The tester doesn't cover it.

## By array type

- **dask**: pint-xarray, MetPy (not run in CI), xclim / icclim (via `registry.convert`), satpy, xMIP (in real use)
- **pandas ExtensionArrays / `pd.NA`**: pint-pandas
- **scipy.sparse**: pairinteraction
- **NumPy masked arrays**: MetPy, spectrochempy, typhon
- **JAX**: dinosaur, jpu
- **PyTorch**: DeepTrack2 (not run in CI)
- **xarray objects via pint-xarray**: pint-xarray, satpy, xMIP, cf-xarray (test skipped)

No project wraps CuPy, pydata `sparse` or uncertainties arrays in Quantities, as far as code search shows.

## Checked, no duck-array use found

The search terms appeared only in docs, lockfiles or unrelated code, or pint is only used with NumPy arrays and scalars:

pyart (fills masked arrays before using pint), ACT, pyTMD, PySDM (pint only for scalar constants; JAX only for `jit`), eradiate, dascore, napari, hyperspy, rosettasciio, pyam, Pyomo, IDAES, geocat-viz, CLIMADA, microsim, py-tdgl, sympl (has a backend abstraction, but no pint+JAX code found), PsyNeuLink, silx, QCElemental, Cantera, physrisk, pyRadPlan (uses scipy.sparse, but not inside Quantities), navis (sparse voxels; pint only for scalar units), pyEQL, pydantic-pint, ucumvert, magicgui, superqt, thermo, chemicals, thermosteam, mendeleev, mp-api, monty, pyiron_atomistics, cp2k-input-tools, htmd, cellpy, yadg, watertap, fluids, ht, tespy, handcalcs, ross, welleng, Roseau_Load_Flow, OCHRE, gplugins, werk24, temoa, flexmeasures, MARIO, lca_algebraic, pymeasure, InstrumentKit, KaithemAutomation, qiskit-metal, pyEPR, ome-types, dit, PyUncertainNumber, autofeat, ChatterBot, stravalib, gopro-dashboard-overlay, tmt, ironic-python-agent, linkml-map, pycalphad, readdy.

## Method and gaps

- GitHub code search for files containing both `pint` and one of `dask`, `sparse`, `masked` (plus `jax`, `torch` and `pint_xarray` for the ~37 priority projects), then the matched lines read by hand. Code search only covers default branches and matches whole tokens, so a project that builds duck-array Quantities in a file that never mentions `pint` (e.g. it imports a registry from elsewhere) could be missed.
- Not checked: Taurus (GitLab) and the 15 skipped projects.
- Cheap coverage gains for the tester: add `dask` to MetPy's `test_deps` (enables its dask-parametrized calc tests), `pint-xarray` to cf-xarray's, and `torch` (CPU) to DeepTrack2's.
