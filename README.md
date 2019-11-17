# eyetracking_data_analyze
This project is developed for analyzing tobii(embeded in HTC vive) eye tracking data. 

We want to know in each frame if participant was looking at specific area in 360 video. In unity, 360 video is projected on the surface of a sphere. The first thing we do is to find hitting point on the sphere according to pose(participant's position in world coordinate), rotation of vr headset and combined gaze direction. Then we convert the point on 3d sphere to point on equirectangular picture. Therefore we are able to know if that point falls in specific area.


## command
```
# convert 360 video to image frams, crop, flipt each image 
python process_video.py /.../scene5  # with mp4 file in this folder

# convert tobii xml to csv which only has time stamp and hitting point coordinates in 2d. 
python process.py /.../data    #see data folder structure 

# combine all data into a csv including reaction time, score, fixation of each scene and each participant
python eye_gaze_processing.py data_dir_name
```

## image data folder structure
```
images
├── demo1                   
│   ├── scene1  
│       ├── frames
│       ├── crops
│       ├── flip
│       ├── video.mp4
│   ├── scene2          
│   └── ...  
├── demo2                    
│   ├── scene1          
│   ├── scene2          
│   └── ...                
|───readme

```

## data folder structure

```
data
├── 001                   
│   ├── PUF_IAT_001     #survey data  
│       ├── ..
│   ├── WSU_ED_001      #eye tracking data  
│       ├── timestamp.xml
│       ├── timestamp2.xml
│       ├── ...
│   ├── WSU_ED_001_EYE      #processed eye tracking data created by process.py 
│       ├── timestamp.csv
│       ├── timestamp2.csv
│       ├── ...
│   └── WSU_HRV_001.xlsx  #heart rate data
│   └── WSU_PR_001.txt    #performance data
│   └── WSU_RT_001.txt    #reaction time data
│   └── WSU_SR_001.mp4    #recording video
├── 002                    
│   ├── ...                       
|───003

```


