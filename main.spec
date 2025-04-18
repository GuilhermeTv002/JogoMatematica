# main.spec
# Gerado para o projeto "Alquimia Suprema"

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[  
        ('imagens/Caldeirao_0.png', 'imagens'),
        ('imagens/Caldeirao_1.png', 'imagens'),
        ('imagens/Caldeirao_2.png', 'imagens'),
        ('imagens/Caldeirao_3.png', 'imagens'),
        ('imagens/Caldeirao_4.png', 'imagens'),
        ('imagens/Caldeirao_5.png', 'imagens'),
        ('imagens/Caldeirao_Vitoria.png', 'imagens'),
        ('imagens/Caldeirao_Perdeu.png', 'imagens'),
        ('imagens/logo.ico', 'imagens')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],  # No additional files here
    exclude_binaries=True,
    name='AlquimiaSuprema',  # O nome da pasta onde os arquivos serão armazenados
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Mude para True se quiser que apareça o terminal junto
    icon='imagens/logo.ico'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AlquimiaSuprema'  # Nome da pasta onde o executável e outros arquivos serão armazenados
)
