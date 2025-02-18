# ShinSokuKun

Python application for forest survey mapping.

Surveying calculation API by Geospatial Information Authority of Japan is used. (https://vldb.gsi.go.jp/sokuchi/surveycalc/main.html)

* `gpx_to_fox.py` Sort gpx tracks and waypoints, then convert to `fox.exe (software for survey drawing)` input text.

## Installation

Instructions on how to install and set up the application.

```bash
# Clone the repository
git clone https://github.com/CleanDiesel/ShinSokuKun.git

# Navigate to the project directory
cd ShinSokuKun

# Install dependencies
pip3 install gpxpy requests
```

## Usage

### gpx_to_fox.py

```bash
# Run the application
python3 gpx_to_fox.py hoge1.gpx (hoge2.gpx hoge3.gpx ...)
# Then follow dialog
```

## Contributing

Guidelines for contributing to the project.

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
