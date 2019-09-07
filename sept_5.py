# Untitled - By: Brady - Tue Sep 3 2019
import uos
import pyb
import sensor, time, image


print("here1")
dir = uos.urandom(3)
print(dir)
dir2 = uos.getcwd()
print(dir2)
print("here2")


#uos.mkdir("/Path")
print("here3")

print("here33")
dir2 = uos.getcwd()
print(dir2)
print("here4")
uos.chdir("/")
snap_img = image.Image("snapshot-384550201.pgm").mask_ellipse()
d0 = snap_img.find_lbp((0, 0, snap_img.width(), snap_img.height()))
lbp_list = []
name_list = []

uos.chdir("/Faces")
for filename in uos.listdir("/Faces"):
  if filename.endswith(".pgm") :
    img = None
    img = image.Image(filename).mask_ellipse()
    d1 = img.find_lbp((0, 0, img.width(), img.height()))
    dist = image.match_descriptor(d0, d1)
    lbp_list.append(dist)
    word = filename
    und_loc = word.index('_')
    word = word[0:(und_loc)]
    #word.split('.')
    print(word)
    name_list.append(word)

    # print(uos.path.join(directory, filename))
    print("Success")
    continue
  else:
    print("ERROR")

print(lbp_list)
print(name_list)
#list_breda = []
#list_breda.append("Breda")
list_set = set(name_list)
# convert the set to the list
unique_list = (list(list_set))
unique_list.reverse()
res = [name_list.index(i) for i in unique_list]

# print result
print("The Match indices list is : " + str(res))
print()
print("name list")
print(name_list)
print()
print("lbp list")
print(lbp_list)
print("unique list")
print(unique_list)

print(res)


i = 0
x=0


total = 0
i = 0
lbp_unique_list = []
while i < (len(res)-1):
    start = res[i]
    end = res[i+1]
    i+= 1
    j = start
    count = 0
    while j < end :
        total += lbp_list[j]
        j+= 1
        count += 1
    lbp_avg = total/count
    print(lbp_avg)
    lbp_unique_list.append(lbp_avg)
    #last = end
    total = 0
    count = 0

last = end

while last  < len(lbp_list):
    total += lbp_list[last]
    last+= 1
    count += 1
lbp_avg = total/count
print(lbp_avg)
lbp_unique_list.append(lbp_avg)

print(lbp_unique_list)
print(min(lbp_unique_list))
name_ind = lbp_unique_list.index(min(lbp_unique_list))
print(name_ind)
print(unique_list[name_ind])
print("The person you are looking at is: " + unique_list[name_ind])
