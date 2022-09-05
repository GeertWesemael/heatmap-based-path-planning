import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import colorsys
import cv2

#colors
def _get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (50 + np.random.rand() * 10)/100.
        saturation = (90 + np.random.rand() * 10)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors

# with open("geertjson", "r") as fp:
    # geertjson = json.load(fp)

# 1280 × 1024 => (1024,1280)
sizex = 800
sizey = 1300
scale = 10
heatmap = np.zeros((int(np.abs(sizey/scale)), int(np.abs(sizex/scale))))

# 1300
# 800

# calculate matrix
plot_width=800
plot_height=1300


#specifying the points in the source image which is to be transformed to the corresponding points in the destination image
srcpts = np.float32([[320,495],[190,810],[1065,803],[800,490]])
destpts = np.float32([[0, 0], [0, plot_height], [plot_width, plot_height], [plot_width, 0]])
# srcpts = np.float32([[400, 529], [320, 790], [865, 795], [715, 529]])
# destpts = np.float32([[0, 0], [0, 2000], [1000, 2000], [1000, 0]])
# srcpts = np.float32([[400, 529], [715, 529], [320, 790], [865, 795]])
# destpts = np.float32([[0, 0], [1000, 0], [0, 2000], [1000, 2000]])
# srcpts = np.float32([[320, 790], [865, 795], [715, 529], [400, 529]])
# destpts = np.float32([[0, 2000], [1000, 2000], [1000, 0], [0, 0]])

#new stuff
#
H,mask = cv2.findHomography(srcpts,destpts)
print(H)

# resmatrix = cv2.getPerspectiveTransform(srcpts, destpts)
# print(resmatrix)
#
# x__ = 575
# y__ = 661
#
# # def transform_points(points):
# #     for i in
#
# new_coord = np.matmul(resmatrix,np.float32([x__,y__,1]))
# print(" tadaaa")
# print(new_coord/new_coord[2])
#
# new_pts = np.float32([ [575,661]]).reshape(-1,1,2)
# new_dst = cv2.perspectiveTransform(new_pts, H)
# print(new_dst)

def transform_point(point):
    new_pts = np.float32([point]).reshape(-1,1,2)
    new_dst = cv2.perspectiveTransform(new_pts, H)
    return new_dst[0][0]

test = transform_point([575,661])
print("test")
print(test)
#
#
# new_points= []
# new_points = cv2.perspectiveTransform(np.array([np.array([x__,y__])]),resmatrix)
# print(new_points)

#
# #find transformation matrix
# resmatrix = cv2.getPerspectiveTransform(srcpts, destpts)
# print(resmatrix)

#get all points
# all_points = np.float32(np.zeros((1,sizex*sizey,2)))
# for index in np.ndindex(sizex,sizey):
#     all_points[0][index[0]+sizex*index[1]][0] = index[0]
#     all_points[0][index[0]+sizex*index[1]][1] = index[1]
#
# #transform points
# all_transformed_points = cv2.perspectiveTransform(all_points, resmatrix)
#
# #dictionary used to transform points
# transform_point = {(int(all_points[0][i][0]),int(all_points[0][i][1])): (int(all_transformed_points[0][i][0]),int(all_transformed_points[0][i][1])) for i in range(len(all_points[0]))}

fake = False

if fake == False:
    with open('geertpickle', 'rb') as f:
        geertpickle = pickle.load(f)
        print("here")
        print(geertpickle)
        print("here")

else:
    # line walking up
    loc1x=575
    loc1y=529
    loc2x=575
    loc2y=793
    ycolist = list(range(loc1y,loc2y))
    pick_list = []
    for i in ycolist:
        pick_list.append([1,loc1x,i,loc1x,i,6])
    # geertpickle = [{'track_bboxes': [[[1,loc1x,loc1y,loc1x,loc1y,6],[1,loc2x,loc2y,loc2x,loc2y,6]]]}]
    geertpickle = [{'track_bboxes': [pick_list]}]




# first_img = geertpickle[0]["track_bboxes"][0] # [[id,(4xcoord),kans op (threshold)], ...]
# img = geertpickle[0]["track_bboxes"][0]
# id = img[0][0]
#
# for box in first_img:
#     centerx = int(np.abs((box[1]+box[3])/2))
#     centery = int(np.abs((box[2]+box[4])/2))
#     heatmap[centery,centerx]+=1

# for i in range(len(geertpickle)):
#     img = geertpickle[i]["track_bboxes"][0]
#     for box in img:
#         if int(box[0]) == 0:
#             continue
#         centerx = int(np.abs((box[1]+box[3])/(2*scale)))
#         centery = int(np.abs((box[2]+box[4])/(2*scale)))
#
#         heatmap[centery,centerx]+=1

# for y in range(len(heatmap)):
#     for x in range(len(heatmap[0])):
#         if(heatmap[y,x]>60):
#             print("here")
#             heatmap[y,x]= 0

# img 1 all paths
plt.imshow(heatmap, cmap='hot', interpolation='nearest')
plt.show()


#### IMG 2

max = 0
for i in range(len(geertpickle)):
    img = geertpickle[i]["track_bboxes"][0]
    for box in img:
        id = box[0]
        if(id>max):
            max = id
print(int(max))

paths = [ [] for _ in range(int(max)+1)]
output_paths = [ {} for _ in range(int(max)+1)]

for i in range(len(geertpickle)):
    img = geertpickle[i]["track_bboxes"][0]
    current_frame = geertpickle[i]["frame"]
    for box in img:
        centerx = int(np.abs((box[1]+box[3])/(2)))
        centery = int(np.abs((box[2]*0.9+box[4]*0.1)/(1)))
        #tranform points

        a = transform_point([centerx,centery])
        #dont transform
        # a = (centerx,centery)
        centerx = a[0]
        centery = sizey-a[1]

        paths[0].append((centerx,centery))

        paths[int(box[0])].append((centerx,centery))

        seconds = current_frame/10.0
        centerx_ = a[0]/100.0
        centery_ = a[1]/100.0
        output_paths[int(box[0])][seconds] = (centerx_,centery_)
print("output paths")
with open('geert_output_paths_big_file', 'wb') as f:
    pickle.dump(output_paths, f)
print("=============")
print(output_paths)

print(paths)
# img 2 all paths different color
fig, ax = plt.subplots()
if not fake:
    paths = paths[1:]
colors = _get_colors(len(paths))

for i in range(len(paths)):
    current_path = paths[i]
    if len(current_path)<2 :
        continue
    codes =  [Path.LINETO for i in range(len(current_path))]
    codes[0] =  Path.MOVETO
    codes[len(current_path)-1] = Path.STOP
    path = Path(current_path,codes)
    patch = patches.PathPatch(path, facecolor='none', edgecolor=colors[i])
    ax.add_patch(patch)
ax.set_xbound(0,sizex)
ax.set_ybound(0,sizey)
plt.show()

# video rectangle => orientation fix:
# reading the input


# videostuff

cap = cv2.VideoCapture("thesistryffmpeg4.mp4")

output = cv2.VideoWriter(
    "output.avi", cv2.VideoWriter_fourcc(*'MPEG'),
  30, (1080, 1920))

while(True):
    ret, frame = cap.read()
    if(ret):

        # adding filled rectangle on each frame
        #linksboven
        cv2.circle(frame, (400,529), 10, (0,0,0), 3)
        #rechtsboven
        cv2.circle(frame, (715,529), 10, (0,255,0), 3)
        #linksbeneden
        cv2.circle(frame, (320,790), 10, (255,0,0), 3)
        #rechtsbeneden
        cv2.circle(frame, (865,793), 10, (255,255,255), 3)

        #linksboven
        cv2.circle(frame, (320,495), 10, (0,0,0), 3)
        #rechtsboven
        cv2.circle(frame, (800,490), 10, (0,255,0), 3)
        #linksbeneden
        cv2.circle(frame, (190,810), 10, (255,0,0), 3)
        #rechtsbeneden
        cv2.circle(frame, (1065,803), 10, (255,255,255), 3)
    # loc1x=360
    # loc1y=529
    # loc2x=360
    # loc2y=793
        cv2.circle(frame, (575,529),10,(0,0,255),3)
        cv2.circle(frame, (575,793),10,(0,0,255),3)

        # writing the new frame in output
        output.write(frame)
        cv2.imshow("output", frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    else:
        break

cv2.destroyAllWindows()
output.release()
cap.release()
