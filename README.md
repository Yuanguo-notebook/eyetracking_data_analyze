# eyetracking_data_analyze
This project is developed for analyzing tobii(embeded in HTC vive) eye tracking data. 

We want to know in each frame if participant was looking at specific area in 360 video. In unity, 360 video is projected on the surface of a sphere. The first thing we do is to find hitting point on the sphere according to pose(participant's position in world coordinate), rotation of vr headset and combined gaze direction. Then we convert the point on 3d sphere to point on equirectangular picture. Therefore we are able to know if that point falls in specific area.
