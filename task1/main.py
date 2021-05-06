import json
import xml.etree.ElementTree as ET
import argparse

class student:
    def __init__(self, id, name, room):
        self.name = name
        self.id = id
        self.room = room

class roomWithStudents():
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.students = []

class fileWorker:
    @staticmethod
    def load_students(fileName):
        students = []
        with open(fileName) as json_file:
            data = json.load(json_file)
            for st in data:
                stud = student(st['id'], st['name'], st['room'])
                students.append(stud)
        return students

    @staticmethod
    def load_rooms(fileName):
        rooms = []
        with open(fileName) as json_file:
            data = json.load(json_file)
            for room in data:
                fullRoom = roomWithStudents(room['id'], room['name'])
                rooms.append(fullRoom)
            json_file.close()
        return rooms
    

    @staticmethod
    def write_to_json(data,fileName):
        with open(fileName+ ".json", 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def write_to_xml(tree,fileName):
        tree.write(fileName + ".xml",encoding='utf-8', xml_declaration=True)

class merger:

    @staticmethod
    def merge_json(students, rooms):
        fullRooms =[]
        students_dict = {}
        for st in students:
            if(st.room in students_dict):
                students_dict[st.room].append(st.__dict__)
            else:
                students_dict[st.room] = [st.__dict__]
        for room in rooms:
            room.students = students_dict[room.id]
            fullRooms.append(room.__dict__)
            
        return fullRooms

    @staticmethod
    def merge_xml(students_list, rooms_list):
        rooms = ET.Element("rooms")
        students_dict = {}

        for st in students_list:
            if(st.room in students_dict):
                students_dict[st.room].append(st)
            else:
                students_dict[st.room] = [st]

        for r in rooms_list:
                room = ET.SubElement(rooms,"room")
                room.set("id", str(r.id))
                room.set("name",str(r.name))
                students_list = ET.SubElement(room,"students")
                local_students_list = students_dict[r.id]
                for s in local_students_list:
                    student = ET.SubElement(students_list,"student")
                    student.set("id", str(s.id))
                    student.set("name",str(s.name))
                    student.set("roomN",str( s.room))

        return ET.ElementTree(rooms)




def mergeFilesToJson(studentsFileName, roomsFileName, outFileName):
        students_list = fileWorker.load_students(studentsFileName)
        rooms = fileWorker.load_rooms(roomsFileName)
        data = merger.merge_json(students_list,rooms)
        fileWorker.write_to_json(data, outFileName)

def mergeFilesToXml(studentsFileName, roomsFileName, outFileName):
        students_list = fileWorker.load_students(studentsFileName)
        rooms = fileWorker.load_rooms(roomsFileName)
        data = merger.merge_xml(students_list,rooms)
        fileWorker.write_to_xml(data, outFileName)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('studentsFile', help='Name of file with students')
    parser.add_argument('roomsFile', help='Name of file with rooms')
    parser.add_argument('format', help='format (json or xml)')

    args = parser.parse_args()

    studentsFileName = args.studentsFile
    roomsFileName = args.roomsFile
    format = args.format
    format = format.lower()

    outFileName = "out"

    if(format == "xml" ):
        mergeFilesToXml(studentsFileName, roomsFileName, outFileName)
    elif(format == "json" ):
        mergeFilesToJson(studentsFileName, roomsFileName, outFileName)
    else:
        print("illigal format ('python main.py -h' for help)")

main()

print("done")