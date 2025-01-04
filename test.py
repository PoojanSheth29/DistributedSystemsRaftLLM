elif option == "3":
                if token:
                    #user_type = "instructor" if "instructor" in token else "student"
                    
                    if "instructor" in token:
                        #user_type = "instructor"
                        #now i am instructor i want to see  file uploaded by student
                        name=input("enter name of student whose file you want to view:  ")
                        name=name+'_token'+'file'
                    else:
                        user_type = "student"
                        # now i have to view files uploaded by instructor
                        name='instructor_token'+'file'

                    
                    #get_assignments(stub, token, user_type)
                    #here i fetch value using function
                    get_something_rajiv(name)

                    #myDict[key] this contains file data
                    #just trial 
                    result=get_something_rajiv(name)
                    print("----")
                    success,filedata=result
                    print(filedata)
                    print("----")
                    #----
                    current_directory ="downloads/"
                    file_path = os.path.join(current_directory, name)#here name refers to file name
                    try:
                        with open(file_path, 'w') as file:
                            file.write(filedata)
                        print(f"File created successfully at: {file_path}")
                    except IOError as e:
                        print(f"Error writing to file: {e}")



                else:
                    print("You must log in first!")

            elif option == "4":