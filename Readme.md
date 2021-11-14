# Health Exporter

Export all your health and lifting metrics to InfluxDB so you can make some pretty graphs on Grafana. At the moment it supports 
- MyFitnessPal
- Repcount
- Garmin **WIP**
- Google Fit **WIP**


## Local Installation
1.  Create a virtualenv

2. Install required packages
```bash
pip install -r requirements.txt
```
3. Run the thing
```python
python main.py
```

## Hosting
I use InfluxDB cloud, Grafana Cloud and Heroku because it runs fine on free tier on all of them. There's a procfile included.


## License
[MIT](https://choosealicense.com/licenses/mit/)
