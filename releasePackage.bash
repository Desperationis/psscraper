echo "WARN: Make sure you have updated the release version of setup.cfg."
read -p "Continue? (y/n): " choice

if ! [[ $choice == "y" ]]
then
	exit 0
fi


echo "Building psscraper..."

if [[ -d src ]]
then
	rm -rf src
fi

if [[ -d dist ]]
then
	rm -rf dist
fi

if ! [[ -d psscraper ]]
then
	echo "ERROR: Could not find psscraper. Maybe try 'git reset --hard'?"
	exit 1
fi

mkdir src
mv psscraper src
python3 -m pip install --upgrade build
python3 -m build


echo "Releasing the package to PyPi.."
python3 -m pip install --upgrade twine
twine upload dist/*
