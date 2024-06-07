# -*- mode: python ; coding: utf-8 -*-

added_files = [
    ('../../src/utilities/*.py', 'utilities'),
    ('../../src/modules/*.py', 'modules')
]

# Collect data files for fake_useragent
fake_useragent_data_files = collect_data_files('fake_useragent')

# Combine both data files lists
combined_data_files = added_files + fake_useragent_data_files


a = Analysis(
    ['../../src/main.py'],
    pathex=[],
    binaries=[],
    datas=combined_data_files,
    hiddenimports=['_cffi_backend'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pyRogue-MacIntel.sh',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
