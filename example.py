from template.create import class_files, cpp_from_h

#generates files dog.cpp and dog.h
class_files(classname = "Dog",
	public_methods =  [	"void bark(float strength, int times)", 
						"int getLegs()"],
	private_methods = [	"int ChangeLegs(int quantity)"]
)


#generates cat.cpp
cpp_from_h("cat.h")
