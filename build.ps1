## Build Script For Python Application

# Setup
$app_name="py_tetris"
$requirements=".\pip_requirements.txt" # Create with pip freeze > pip_requirements.txt
$path_to_build_util="c:\Users\admin\AppData\Local\Programs\Python\Python37\Lib\site-packages\PyInstaller" # Path to PyInstaller (creates exe from python source)
$exta_files=@('*.json','*.md')

Write-Output "Install python requirements.."
& pip3.7.exe install -r $requirements

Write-Output "Remove Previous Versions"
if (Test-Path .\dist){
    Remove-Item .\dist -Recurse -Force
}

Write-Output "Building Application..."
& python.exe $path_to_build_util .\py_tetris.py --onefile

# Check the Application built OK
if (Test-Path .\dist) {
    # Deploy files into dist folder
    Copy-Item .\game_assets .\dist -Recurse -Force
    # Deploy any extras defined earlier
    foreach ($file_type in $exta_files){
        Copy-Item $file_type .\dist\ -Force
    }
}
else {
    Write-Output "Error Failed to build application..."
}

# Package Application
Compress-Archive -Path .\dist -DestinationPath .\dist\$app_name.zip