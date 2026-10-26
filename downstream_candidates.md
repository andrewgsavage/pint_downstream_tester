# Pint downstream candidates

Projects that use pint in their own code, as candidates for the downstream tester.

How the list was built (2026-10-24):

1. Scraped GitHub's "Used by" (packages) list for hgrecco/pint: 906 packages, 152 with at least 50 stars.
2. Kept those pushed in the last year, not archived or forks, with `pint` in a root dependency file.
3. Searched each repo's code and dropped those that only declare pint without importing it in library code.
4. Added projects GitHub's dependency graph misses (marked †): Cantera, OpenFE, and the pint docs ecosystem page's ucumvert and Taurus.

## Wrappers and integrations

| Project | Stars | Description |
|---|---:|---|
| [magicgui](https://github.com/pyapp-kit/magicgui) | 510 | Builds GUIs from type annotations, with pint quantity widgets |
| [superqt](https://github.com/pyapp-kit/superqt) | 295 | Extra Qt widgets, including a pint quantity spinbox |
| [pint-pandas](https://github.com/hgrecco/pint-pandas) | 189 | Pandas extension array for pint quantities |
| [cf-xarray](https://github.com/xarray-contrib/cf-xarray) | 183 | CF-conventions accessor for xarray; adds a CF-aware pint unit registry |
| [pint-xarray](https://github.com/xarray-contrib/pint-xarray) | 120 | Unit-aware xarray objects via a `.pint` accessor |
| [pydantic-pint](https://github.com/tylerh111/pydantic-pint) | 57 | Pydantic field types for pint quantities |
| [jpu](https://github.com/dfm/jpu) | 54 | Pint units for JAX arrays |
| [ucumvert](https://github.com/dalito/ucumvert) † | 17 | UCUM unit-code parser and converter to pint units |

## Weather, climate and earth science

| Project | Stars | Description |
|---|---:|---|
| [MetPy](https://github.com/Unidata/MetPy) | 1,450 | Meteorology calculations, I/O and plotting, built on pint units |
| [satpy](https://github.com/pytroll/satpy) | 1,212 | Earth-observation satellite data processing |
| [pyart](https://github.com/ARM-DOE/pyart) | 609 | Weather radar data toolkit |
| [climada_python](https://github.com/CLIMADA-project/climada_python) | 483 | Climate risk and adaptation modelling |
| [xclim](https://github.com/Ouranosinc/xclim) | 408 | Climate indicators computed from xarray data with unit checking |
| [dinosaur](https://github.com/neuralgcm/dinosaur) | 338 | Differentiable atmospheric dynamical core for NeuralGCM |
| [invest](https://github.com/natcap/invest) | 258 | Models that map and value ecosystem services |
| [underworld2](https://github.com/underworldcode/underworld2) | 217 | Parallel finite-element geodynamics code |
| [pyTMD](https://github.com/pyTMD/pyTMD) | 212 | Tidal prediction |
| [xMIP](https://github.com/jbusecke/xMIP) | 206 | Preprocessing CMIP6 climate model data with pint-xarray |
| [ACT](https://github.com/ARM-DOE/ACT) | 193 | Atmospheric measurement data toolkit |
| [dascore](https://github.com/DASDAE/dascore) | 173 | Distributed fibre-optic sensing data analysis |
| [eradiate](https://github.com/eradiate/eradiate) | 101 | Radiative transfer model for Earth observation |
| [icclim](https://github.com/cerfacs-globc/icclim) | 93 | Climate indices calculation (builds on xclim) |
| [PySDM](https://github.com/open-atmos/PySDM) | 92 | Particle-based cloud microphysics simulation |
| [anemoi-datasets](https://github.com/ecmwf/anemoi-datasets) | 88 | Datasets for machine-learning weather forecasting |
| [physrisk](https://github.com/os-climate/physrisk) | 71 | Physical climate risk calculation engine |
| [geocat-viz](https://github.com/NCAR/geocat-viz) | 66 | Plotting helpers for geoscience data |
| [typhon](https://github.com/atmtools/typhon) | 62 | Tools for atmospheric research |
| [pywatershed](https://github.com/DOI-USGS/pywatershed) | 56 | Hydrologic model |
| [sympl](https://github.com/mcgibbon/sympl) | 52 | Toolkit for building Earth-system models |

## Chemistry and materials

| Project | Stars | Description |
|---|---:|---|
| [cantera](https://github.com/Cantera/cantera) † | 875 | Chemical kinetics, thermodynamics and transport; `cantera.with_units` uses pint |
| [thermo](https://github.com/CalebBell/thermo) | 795 | Thermodynamics and phase equilibrium |
| [pycalphad](https://github.com/pycalphad/pycalphad) | 424 | CALPHAD thermodynamic modelling and phase diagrams |
| [openfe](https://github.com/OpenFreeEnergy/openfe) † | 344 | Free energy calculation toolkit |
| [chemicals](https://github.com/CalebBell/chemicals) | 314 | Chemical property database and correlations |
| [mendeleev](https://github.com/lmmentel/mendeleev) | 307 | Properties of elements, ions and isotopes |
| [htmd](https://github.com/Acellera/htmd) | 277 | Molecular discovery and simulation environment |
| [QCElemental](https://github.com/MolSSI/QCElemental) | 203 | Periodic table, physical constants and molecule parsing for quantum chemistry |
| [spectrochempy](https://github.com/spectrochempy/spectrochempy) | 187 | Spectroscopic data processing and modelling |
| [api](https://github.com/materialsproject/api) | 179 | Materials Project API client |
| [chembench](https://github.com/lamalab-org/chembench) | 147 | Benchmark of LLM chemistry knowledge |
| [nomad](https://github.com/FAIRmat-NFDI/nomad) | 122 | NOMAD materials-science data platform backend |
| [cellpy](https://github.com/jepegit/cellpy) | 112 | Battery cell test data processing |
| [monty](https://github.com/materialyzeai/monty) | 85 | Python utilities used by pymatgen; pint-aware JSON serialisation |
| [pyEQL](https://github.com/KingsburyLab/pyEQL) | 81 | Solution chemistry (already tested here at 0.3.1) |
| [thermosteam](https://github.com/BioSTEAMDevelopmentGroup/thermosteam) | 80 | Thermodynamic engine for BioSTEAM |
| [readdy](https://github.com/readdy/readdy) | 65 | Particle reaction-diffusion simulator |
| [cp2k-input-tools](https://github.com/cp2k/cp2k-input-tools) | 63 | CP2K input file parsing and validation |
| [wepy](https://github.com/ADicksonLab/wepy) | 61 | Weighted-ensemble molecular simulation |
| [aiida-common-workflows](https://github.com/aiidateam/aiida-common-workflows) | 60 | Common workflow interfaces across quantum codes (AiiDA) |
| [yadg](https://github.com/dgbowl/yadg) | 57 | Parser for experimental instrument data files |
| [pyiron_atomistics](https://github.com/pyiron/pyiron_atomistics) | 55 | Atomistic simulation environment |

## Engineering and optimisation

| Project | Stars | Description |
|---|---:|---|
| [handcalcs](https://github.com/connorferster/handcalcs) | 5,807 | Renders Python calculations as LaTeX, with pint units |
| [pyomo](https://github.com/Pyomo/pyomo) | 2,551 | Optimisation modelling language; pint backs its units system |
| [fluids](https://github.com/CalebBell/fluids) | 462 | Fluid dynamics calculations |
| [tespy](https://github.com/oemof/tespy) | 426 | Thermal engineering system simulation |
| [idaes-pse](https://github.com/IDAES/idaes-pse) | 351 | Process systems engineering framework on Pyomo |
| [ht](https://github.com/CalebBell/ht) | 258 | Heat transfer calculations |
| [ross](https://github.com/petrobras/ross) | 214 | Rotordynamic analysis |
| [gflabel](https://github.com/ndevenish/gflabel) | 172 | Generates 3D-printable gridfinity labels |
| [welleng](https://github.com/jonnymaserati/welleng) | 164 | Well and drilling engineering tools |
| [watertap](https://github.com/watertap-org/watertap) | 116 | Water treatment process modelling on IDAES |
| [pyansys-geometry](https://github.com/ansys/pyansys-geometry) | 99 | Python client for Ansys Geometry services |
| [werk24-python](https://github.com/W24-Service-GmbH/werk24-python) | 94 | Client for automated technical-drawing processing |
| [OCHRE](https://github.com/NatLabRockies/OCHRE) | 75 | Building energy modelling |
| [Roseau_Load_Flow](https://github.com/RoseauTechnologies/Roseau_Load_Flow) | 66 | Multi-phase power load flow solver |
| [gplugins](https://github.com/gdsfactory/gplugins) | 62 | Simulation plugins for the gdsfactory chip-layout tool |

## Energy systems and integrated assessment

| Project | Stars | Description |
|---|---:|---|
| [pyam](https://github.com/IAMconsortium/pyam) | 291 | Analysis and visualisation of energy and climate scenarios |
| [flexmeasures](https://github.com/FlexMeasures/flexmeasures) | 212 | Energy flexibility optimisation platform |
| [temoa](https://github.com/TemoaProject/temoa) | 115 | Energy system optimisation; pint-based unit checking |
| [lca_algebraic](https://github.com/oie-mines-paristech/lca_algebraic) | 58 | Parametric life-cycle assessment on brightway2 |
| [NEMO](https://github.com/bje-/NEMO) | 53 | Electricity market optimiser |
| [MARIO](https://github.com/it-is-me-mario/MARIO) | 53 | Input-output and supply-use modelling |

## Lab instruments and control

| Project | Stars | Description |
|---|---:|---|
| [pymeasure](https://github.com/pymeasure/pymeasure) | 791 | Scientific instrument control and experiments |
| [InstrumentKit](https://github.com/instrumentkit/InstrumentKit) | 279 | Communicating with lab equipment over various buses |
| [KaithemAutomation](https://github.com/EternityForest/KaithemAutomation) | 74 | Home automation / SCADA |
| [taurus](https://gitlab.com/taurus-org/taurus) † | 12 (GitLab) | Control-system and SCADA GUI framework (GitLab) |

## Physics and quantum

| Project | Stars | Description |
|---|---:|---|
| [qiskit-metal](https://github.com/qiskit-community/qiskit-metal) | 430 | Design and analysis of superconducting quantum chips |
| [pyEPR](https://github.com/zlatko-minev/pyEPR) | 211 | Energy-participation analysis of quantum microwave circuits |
| [py-tdgl](https://github.com/loganbvh/py-tdgl) | 62 | Time-dependent Ginzburg-Landau superconductor simulation |
| [pairinteraction](https://github.com/pairinteraction/pairinteraction) | 54 | Rydberg atom interaction calculator |
| [pyRadPlan](https://github.com/e0404/pyRadPlan) | 52 | Radiotherapy treatment planning |

## Imaging and data analysis

| Project | Stars | Description |
|---|---:|---|
| [napari](https://github.com/napari/napari) | 2,785 | Multi-dimensional image viewer |
| [hyperspy](https://github.com/hyperspy/hyperspy) | 585 | Multi-dimensional data analysis, e.g. electron microscopy |
| [dit](https://github.com/dit/dit) | 580 | Information theory |
| [autofeat](https://github.com/cod3licious/autofeat) | 546 | Automated feature engineering with unit-aware features |
| [DeepTrack2](https://github.com/DeepTrackAI/DeepTrack2) | 247 | Synthetic microscopy data and deep learning |
| [silx](https://github.com/silx-kit/silx) | 167 | Synchrotron data I/O and visualisation |
| [navis](https://github.com/navis-org/navis) | 139 | Neuroanatomy data analysis |
| [PsyNeuLink](https://github.com/PrincetonUniversity/PsyNeuLink) | 117 | Cognitive neuroscience modelling |
| [PyUncertainNumber](https://github.com/leslieDLcy/PyUncertainNumber) | 96 | Uncertainty analysis with uncertain numbers |
| [rosettasciio](https://github.com/hyperspy/rosettasciio) | 73 | Reads and writes scientific data formats |
| [ome-types](https://github.com/imaging-formats/ome-types) | 68 | Python dataclasses for the OME microscopy data model |
| [palom](https://github.com/labsyspharm/palom) | 66 | Alignment of large microscopy image mosaics |
| [microsim](https://github.com/tlambert03/microsim) | 57 | Light microscopy simulation |

## Applications and tools (lighter pint use)

| Project | Stars | Description |
|---|---:|---|
| [ChatterBot](https://github.com/gunthercox/ChatterBot) | 14,521 | Conversational chatbot engine; pint drives unit-conversion answers |
| [fixinventory](https://github.com/someengineering/fixinventory) | 2,086 | Cloud asset inventory and security |
| [stravalib](https://github.com/stravalib/stravalib) | 1,002 | Strava API client; returns pint quantities |
| [gopro-dashboard-overlay](https://github.com/time4tea/gopro-dashboard-overlay) | 589 | Renders GPS data overlays onto GoPro video |
| [tmt](https://github.com/teemtee/tmt) | 158 | Test management tool (Fedora/RHEL) |
| [ironic-python-agent](https://github.com/openstack/ironic-python-agent) | 133 | Bare-metal provisioning agent for OpenStack |
| [robotoff](https://github.com/openfoodfacts/robotoff) | 117 | Prediction service for Open Food Facts |
| [linkml-map](https://github.com/linkml/linkml-map) | 50 | Mapping between LinkML schemas, including unit conversion |
| [pycram](https://github.com/cram2/pycram) | 50 | Cognitive robot control framework |

## Dropped: pint declared but not used in library code

- [deeptime](https://github.com/deeptime-ml/deeptime): no pint in code
- [femwell](https://github.com/HelgeGehring/femwell): pint only in a docs example
- [IMAS-Python](https://github.com/iterorganization/IMAS-Python): pint only in docs
- [neuropythy](https://github.com/noahbenson/neuropythy): pint only in requirements
- [message_ix](https://github.com/iiasa/message_ix): pint only in tests; it gets units through ixmp/genno
- [qtile-extras](https://github.com/elParaguayo/qtile-extras): pint only via stravalib
- [climt](https://github.com/CliMT/climt): no direct use; units come through sympl
