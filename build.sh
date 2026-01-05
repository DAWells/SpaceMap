echo "Download solar system"
python -m plot.solarWindRose.download_solar_system
echo "Preprocess solar system"
python -m plot.solarWindRose.preprocess_solar_system
echo "Plot solar system"
python -m plot.solarWindRose.plot_solar_system

mkdir public
cp data/images/* public
cp webpage/index.html
cp webpage/completetemplate.html public
cp webpage/style.css public

echo "Build complete"