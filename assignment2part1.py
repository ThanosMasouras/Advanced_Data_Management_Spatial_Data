import csv

def get_data():
	print("getting data from tiger_roads.csv")
	with open('tiger_roads.csv', newline='') as csvfile:
	    id = 0
	    data = []    
	    maxX = float('-inf')
	    maxY = float('-inf')
	    minX = float('inf')
	    minY = float('inf')
	    reader = csv.reader(csvfile)
	    next(reader)
	    
	    for row in reader:
	        id+=1
	        coords_row = []
	        MBRminX = float('inf')
	        MBRminY = float('inf')
	        MBRmaxX = float('-inf')
	        MBRmaxY = float('-inf')
	        for coord_pair in row:
	            coord_split = coord_pair.split()
	            coord_floats = []
	            for coord in coord_split:
	                coord_floats.append(float(coord))

	            if coord_floats[0] < MBRminX:
	                MBRminX = coord_floats[0]
	            if coord_floats[0] > MBRmaxX:
	                MBRmaxX = coord_floats[0]
	            if coord_floats[1] < MBRminY:
	                MBRminY = coord_floats[1]
	            if coord_floats[1] > MBRmaxY:
	                MBRmaxY = coord_floats[1]
	                
	            if coord_floats[0] > maxX:
	                maxX = coord_floats[0]
	            if coord_floats[0] < minX:
	                minX = coord_floats[0]
	            if coord_floats[1] > maxY:
	                maxY = coord_floats[1]
	            if coord_floats[1] < minY:
	                minY = coord_floats[1]
	                
	            coords_row.append(coord_floats)
	        
	        triplet = [id,[MBRminX,MBRminY],[MBRmaxX,MBRmaxY],coords_row]
	        data.append(triplet)
	    return data,maxX,maxY,minX,minY

def create_grid(data,maxX,maxY,minX,minY):
	num_cells = 10
	grid = {}
	cellx_range = (maxX - minX)/10
	celly_range = (maxY - minY)/10
	for i in range(num_cells):
	    for j in range(num_cells):
	        cell_id = (minX + i*cellx_range, minY + j*celly_range)
	        grid[cell_id] = []

	for row in data:
	    MBRminX = row[1][0]
	    MBRminY = row[1][1]
	    MBRmaxX = row[2][0]
	    MBRmaxY = row[2][1]
	    for i in range(100):
	        cell_coordX = list(grid)[i][0]
	        cell_coordY = list(grid)[i][1]
	        if MBRminX >= cell_coordX and MBRminY >= cell_coordY and MBRminX <= cell_coordX + cellx_range and MBRminY <= cell_coordY + celly_range:
	            minMBRcell = i
	        if MBRmaxX >= cell_coordX and MBRmaxY >= cell_coordY and MBRmaxX <= cell_coordX + cellx_range and MBRmaxY <= cell_coordY + celly_range:
	            maxMBRcell = i
	    if minMBRcell == maxMBRcell: 
	        id_coord_array = grid[list(grid)[minMBRcell][0],list(grid)[minMBRcell][1]]
	        id_coord_array.append(row[0])
	        grid[list(grid)[minMBRcell][0],list(grid)[minMBRcell][1]] = id_coord_array
	    else:
	        difference_x = (maxMBRcell%10) - (minMBRcell%10)
	        difference_y = (maxMBRcell//10) - (minMBRcell//10)
	        for i in range(difference_y+1):
	            for j in range(difference_x+1):
	                id_coord_array = grid[list(grid)[minMBRcell + j + i*10][0],list(grid)[minMBRcell + j + i*10][1]]
	                id_coord_array.append(row[0])
	                grid[list(grid)[minMBRcell + j + i*10][0],list(grid)[minMBRcell + j + i*10][1]] = id_coord_array
	return grid    

def create_dir_file(grid,maxX,maxY,minX,minY):
	i = 0
	j = 0
	with open("grid.dir", "w") as f:
	    f.write(f"{minX} {maxX} {minY} {maxY}\n")
	    for cell in grid:
	        f.write(f"{i} {j} {len(grid[cell])}\n")
	        j+= 1
	        if j==10:
	            i+=1
	            j= 0
	    f.close()
	print("grid.dir creation finished")

def create_grd_file(grid,data):
	with open("grid.grd", "w") as f:
	    for cell in grid:
	        if len(grid[cell]) != 0:
	            for id in grid[cell]:
	                f.write(f"{id}")
	                f.write(f",{data[id-1][1][0]} {data[id-1][1][1]}")
	                f.write(f",{data[id-1][2][0]} {data[id-1][2][1]}")
	                for cordinates in data[id-1][3]:
	                        for cord in cordinates:
	                            f.write(f",{cord}")
	                f.write(f" \n")
	print("grid.grd creation finished")

def main():
	data,maxX,maxY,minX,minY = get_data()
	grid = create_grid(data,maxX,maxY,minX,minY)
	create_dir_file(grid,maxX,maxY,minX,minY)
	create_grd_file(grid,data)
main()
