#ATHANASIOS MASOURAS - 2752
import sys
def get_data_from_dir():
	with open('grid.dir', 'r') as file:
		first_line = file.readline().strip()
		number_of_ids_in_cells = []
		for line in file:
			row = list(map(int,line.strip().split()))
			third_column = row[2]
			number_of_ids_in_cells.append(third_column)
			
	grid_min_max = list(map(float, first_line.split()))
	minX = grid_min_max[0]
	maxX = grid_min_max[1]
	minY = grid_min_max[2]
	maxY = grid_min_max[3]

	return number_of_ids_in_cells,maxX,maxY,minX,minY

def get_data_from_grd(number_of_ids_in_cells,maxX,maxY,minX,minY):
	num_cells = 10
	grid = {}
	cellx_range = (maxX - minX)/10
	celly_range = (maxY - minY)/10

	for i in range(num_cells):
		for j in range(num_cells):
			cell_id = (minX + i*cellx_range, minY + j*celly_range)
			grid[cell_id] = []

	info_cells_on_grid = []
	with open("grid.grd") as f:
		for line in f:
			elements = line.strip().split(",")
			float_list = []
			for i, element in enumerate(elements):
				if " " in element:
					sub_elements = element.split()
					float_list += [float(sub_elements[0]), float(sub_elements[1])]
				else:
					float_list.append(float(element))
			info_cells_on_grid.append(float_list)


	i = 0
	counter = 0
	for cell in grid:
		if number_of_ids_in_cells[i] != 0:
			for j in range(number_of_ids_in_cells[i]):
				grid[cell].append(int(info_cells_on_grid[j+counter][0]))
		counter = counter + number_of_ids_in_cells[i]
		i=i+1

	return grid, info_cells_on_grid

def get_query_from_txt(txt_file, query):
	with open(txt_file, 'r') as file:
		for i in range(query-1):
			file.readline()
		line = file.readline().strip()
		first_query = [float(x) for x in line.split(',')[1].split()]
	window_minX = first_query[0]
	window_maxX = first_query[1]
	window_minY = first_query[2]
	window_maxY = first_query[3]

	return window_minX,window_maxX,window_minY,window_maxY

def window_intersections(grid,info_cells_on_grid,window_minX,window_maxX,window_minY,window_maxY,maxX,maxY,minX,minY):
	ids_result = []
	cells_checked = 0
	cellx_range = (maxX - minX)/10
	celly_range = (maxY - minY)/10
	for i in range(100):
		cell_coordX = list(grid)[i][0]
		cell_coordY = list(grid)[i][1]
		if window_minX >= cell_coordX and window_minY >= cell_coordY and window_minX <= cell_coordX + cellx_range and window_minY <= cell_coordY + celly_range:
			minMBRcell = i
		if window_maxX >= cell_coordX and window_maxY >= cell_coordY and window_maxX <= cell_coordX + cellx_range and window_maxY <= cell_coordY + celly_range:
			maxMBRcell = i
	found = False
	if minMBRcell == maxMBRcell:
		cells_checked = 1
		ids_of_cell = grid[list(grid)[minMBRcell]]
		for id in ids_of_cell:
			while(found == False):
				if info_cells_on_grid[i][0] == id:
					id_minX = info_cells_on_grid[i][1]
					id_minY = info_cells_on_grid[i][2]
					id_maxX = info_cells_on_grid[i][3]
					id_maxY = info_cells_on_grid[i][4]
					if (window_minX <= id_maxX and window_minY <= id_maxY) and (window_maxX >= id_minX and window_maxY >= id_minY):
						if id not in ids_result:
							ids_result.append(id)
					elif (window_minX <= id_minX and window_minY <= id_minY) and (window_maxX >= id_maxX and window_maxY >= id_maxY):
						if id not in ids_result:
							ids_result.append(id)
					found = True
				i = i + 1
			found = False
	else:
		difference_x = (maxMBRcell%10) - (minMBRcell%10)
		difference_y = (maxMBRcell//10) - (minMBRcell//10)
		for x in range(difference_y+1):
			for y in range(difference_x+1):
				cells_checked += 1
				ids_of_cell = grid[list(grid)[minMBRcell + x + y*10]]
				for id in ids_of_cell:
					while(found == False):
						if info_cells_on_grid[i][0] == id:
							id_minX = info_cells_on_grid[i][1]
							id_minY = info_cells_on_grid[i][2]
							id_maxX = info_cells_on_grid[i][3]
							id_maxY = info_cells_on_grid[i][4]
							if (window_minX <= id_maxX and window_minY <= id_maxY) and (window_maxX >= id_minX and window_maxY >= id_minY):
								if id not in ids_result:
									ids_result.append(id)
							elif (window_minX <= id_minX and window_minY <= id_minY) and (window_maxX >= id_maxX and window_maxY >= id_maxY):
								if id not in ids_result:
									ids_result.append(id)
							found = True
						i = i + 1
					found = False
	return ids_result, cells_checked

def intersect(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    if x2 - x1 != 0:
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
    else:
        m1 = float('inf')
        b1 = x1

    if x4 - x3 != 0:
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3
    else:
        m2 = float('inf')
        b2 = x3

    if m1 == m2:
        return False

    if m1 != float('inf') and m2 != float('inf'):
        x_intersect = (b2 - b1) / (m1 - m2)
    else:
        x_intersect = b1 if m1 == float('inf' )else b2
        
    if m1 != float('inf'):
        y_intersect = m1 * x_intersect + b1
    else:
        y_intersect = m2 * x_intersect + b2

    if (min(x1, x2) <= x_intersect <= max(x1, x2)) and (min(y1, y2) <= y_intersect <= max(y1, y2)) and (min(x3, x4) <= x_intersect <= max(x3, x4)) and (min(y3, y4) <= y_intersect <= max(y3, y4)):
        return True

    return False


def get_ids_coords(id,info_cells_on_grid):
    ids_coords=[]
    for i in info_cells_on_grid:
        if i[0] == id:
            for j in range(5,len(i),2):
                ids_coords.append([i[j],i[j+1]])
        
    return ids_coords


def calculate_mbr_points(minMBRx, minMBRy, maxMBRx, maxMBRy):
    mbr_points = []
    mbr_points.append([minMBRx, minMBRy])
    mbr_points.append([minMBRx, maxMBRy])
    mbr_points.append([maxMBRx, maxMBRy])
    mbr_points.append([maxMBRx, minMBRy])
    return mbr_points

def refinement_stage(info_cells_on_grid,ids_result,get_ids_coords,window_minX,window_maxX,window_minY,window_maxY):
	window_points = calculate_mbr_points(window_minX,window_minY,window_maxX,window_maxY)
	ids_refinement_result = []
	for id in ids_result:
	    linestrings = get_ids_coords(id,info_cells_on_grid)
	    for i in range(len(linestrings)-1):
	        coord = list(linestrings[i+1])+list(linestrings[i])
	        if intersect(coord,window_points[0] + window_points[1]) or intersect(coord,window_points[1] + window_points[2]) or intersect(coord,window_points[2] + window_points[3]) or intersect(coord,window_points[3] + window_points[0]):
	            if id not in ids_refinement_result:
	            	ids_refinement_result.append(id)
	return ids_refinement_result

def get_nlines_of_file(txt_file):
	with open(txt_file, 'r') as file:
		lines = file.readlines()
	num_lines = len(lines)
	return num_lines

def print_results(ids,cells_checked,query):
	print(f"Query {query} results:")
	print(f"{' '.join(map(str, ids))}")
	print(f"Cells: {cells_checked}")
	print(f"Results: {len(ids)}")
	print(f"----------")

def main():
	txt_file = sys.argv[1]
	number_of_ids_in_cells,maxX,maxY,minX,minY = get_data_from_dir()
	grid, info_cells_on_grid = get_data_from_grd(number_of_ids_in_cells,maxX,maxY,minX,minY)
	num_lines = get_nlines_of_file(txt_file)
	for i in range(1,num_lines+1):
		window_minX,window_maxX,window_minY,window_maxY = get_query_from_txt(txt_file, i)
		ids_result, cells_checked = window_intersections(grid,info_cells_on_grid,window_minX,window_maxX,window_minY,window_maxY,maxX,maxY,minX,minY)
		ids_refinement_result = refinement_stage(info_cells_on_grid,ids_result,get_ids_coords,window_minX,window_maxX,window_minY,window_maxY)
		print_results(ids_refinement_result,cells_checked,i)
main()