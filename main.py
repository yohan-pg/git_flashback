import gitimport
import importlib 
import pygit2
import sys 

print(sys.path_hooks)
print(gitimport.repository_path('.', rev="79398a7856f9537c2c3a90402c48a62c61e902f7"))

# print(
#     importlib.util.find_spec(
#         "dsa2", 
#         gitimport.repository_path('.git', rev="79398a7856f9537c2c3a90402c48a62c61e902f7")
#     )
# )

# gitimport.add_repository_to_path('.')
# import dsa
# print(gitimport.repository_path('.'))
# importlib.import_module("dsa", gitimport.repository_path('.'))

# gitimport.add_repository_to_path('.', rev='v1')
