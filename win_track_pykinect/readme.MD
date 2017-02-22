This is a first attempt to obtain angles of the knees by tracking with kinect v1.
## <a name="fetch-build"></a>Fetch & Build
To implement this on windows follow the requirements:
- Install git [here](https://git-scm.com/download/win)
- Install python 2.7 [here](https://www.python.org/downloads/release/python-2713/)
- Install the Kinect SDK 1.0 [here](http://www.microsoft.com/en-us/download/details.aspx?id=28782)
- Install Anaconda for python 2.7 [here](https://www.continuum.io/downloads#windows)
- Clone this repository
- Use "win_environment.yml" to create the enviroment
- Active the enviroment and run 'knee_angle.py'

## <a name="fetch-build"></a>

    C:\>git clone https://github.com/lab-info-saude/ohpera.git
    C:\>cd ohpera\win_track_pykinect
    C:\cd ohpera\win_track_pykinect>conda env create -f win_environment.yml
    C:\cd ohpera\win_track_pykinect> set PATH=%PATH%;C:\python27;C:\Python27\Lib\site-packages\pip
    C:\cd ohpera\win_track_pykinect> activate mocap
    C:\cd ohpera\win_track_pykinect> python knee_angle.py

# More Information
For more information of this methods check ["Possibly Wrong"](https://possiblywrong.wordpress.com/2012/11/04/kinect-skeleton-tracking-with-visual-python/#comment-3129) blog.

## <a name="fetch-build"></a>Specifies the various skeleton joints.

    >>>skeleton.joints = [
    HipCenter = 0,
    Spine = 1,
    ShoulderCenter = 2,
    Head = 3,
    ShoulderLeft = 4,
    ElbowLeft = 5,
    WristLeft = 6,
    HandLeft = 7,
    ShoulderRight = 8,
    ElbowRight = 9,
    WristRight = 10,
    HandRight = 11,
    HipLeft = 12,
    KneeLeft = 13,
    AnkleLeft = 14,
    FootLeft = 15,
    HipRight = 16,
    KneeRight = 17,
    AnkleRight = 18,
    FootRight = 19,
    ]
