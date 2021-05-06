class Version:
    def __init__(self, version):
        self.value = version.lower() 
        self.value_len = len(version)
        self.version_split_list = version.split(".")

    def __eq__(self, other):
        return self.compare_version(other.value) == 0 

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.compare_version(other.value) == -1 
    
    def __le__(self, other):
        return self.compare_version(other.value) != 1
    
    def __gt__(self, other):
        return self.compare_version(other.value) == 1 

    def __ge__(self, other): 
         return self.compare_version(other.value) != -1

    '''This method compares versions and returns:
        1 - if second argument elder than first
        0 - if arguments are equal
        -1 -  if first argument elder than second '''

    def compare_version(self, version2):

        version2 = version2.lower()
        if(self.value == version2):
            return 0

        compare_result = 0
        version_split_list2 = version2.split(".")
        i = 0
        min_len = len(version_split_list2)

        if(self.value_len < min_len):
            min_len = len(self.version_split_list)

        while (i<min_len and compare_result == 0):

            if self.version_split_list[i].isdigit() and version_split_list2[i].isdigit() :
                compare_result = self.compare_num_version(self.version_split_list[i], version_split_list2[i])
           
            else:
                compare_result = self.compare_str_version(self.version_split_list[i], version_split_list2[i])

            i+=1

        return compare_result

    '''This method compares version parts with digits only'''

    def compare_num_version(self,str1,str2):
        if str1 > str2:
            return 1
        elif str1 < str2:
            return -1
        else:
            return 0

    '''This method compare version parts with all symbols (compare every letter)'''

    def compare_str_version(self,str1,str2):

        if(str1 == str2):
            return 0

        i = 0
        min_len = len(str2)
        if(len(str1) < min_len):
            min_len = len(str1)
        
        while (i<min_len):
            #if only one char is number (older version - with char (1095b < 10954b ))
            if str1[i].isalpha() ^ str2[i].isalpha():
                if str1[i].isalpha():
                    return -1
                else:
                    return 1

            elif str1[i]>str2[i] :
                return 1

            elif str1[i] < str2[i]:
                return -1

            i+=1
        
        return self.compare_len(str1,str2)

    def compare_len(self,str1,str2):
            if len(str1) < len(str2):
                return 1
            elif len(str1) > len(str2):
                return -1
            else:
                return 0

    


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"

if __name__ == "__main__":
    main()
