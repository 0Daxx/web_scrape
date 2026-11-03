from scrapling.fetchers import Fetcher
import requests 
from scrapling.spiders import Spider , Response

def fn2():
    
    class RoadmapSpider(Spider):
        name="roadmap"
        start_urls = ["https://roadmap.sh/frontend/projects"]
        # allowed_domains= {"https://roadmap.sh"}
    
        async def parse(self,response : Response):

            for project in response.css("span.my3"):
                yield {
                    "project_name": project.css("span.mb1::text").get(""),
                    "project_description": project.css("span.text-sm::text").get(""),
                }
        

    result = RoadmapSpider().start()
    print("result.items , ", result.items)
    print()

    for item in result.items:
        with open('roadmap.json', 'w') as f:
            f.write(str(item))


def fn3():
    page = Fetcher.get('https://roadmap.sh/frontend/projects')
    print(page)
    with open ('roadmap.markdown', 'w') as f:
        f.write(page.markdown())

def fetch_project_details():
    page = Fetcher.get('https://roadmap.sh/projects/task-tracker')
    # print(page)

    # page.html_content
    with open ('project.md', 'w') as f:
        f.write(page.markdown())
    # with open ('project_html.txt', 'w') as f:
    #     f.write(page.html_content)
    
    
def fn1():
    page = Fetcher.get('https://roadmap.sh/')


    # quotes = page.css('.quote .text::text').getall()
    print(page)

    with open ('roadmap.markdown', 'w') as f:
        f.write(page.markdown())

    # print(page.markdown())
# print(page.markdown() ('title::text').getall())


def clean_project_md():

    with open('project.md', 'r') as f:
        content = f.readlines()
        # print("content , ", content)
        # delete 2 - 12 lines
        content = content[0:1] + content[12:]  # Keep lines after the 12th line

        # find "Start building and delete 13 lines after it"
        for i, line in enumerate(content):
            if "Start building," in line:
                # Delete the next 13 lines after this line
                del content[i + 1:i + 14]
                break
        
        # Find "Happy Coding and delete everything after it"
        for i, line in enumerate(content):
            if "Happy coding!" in line:
                # Delete everything after this line
                content = content[:i + 1]
                break
        with open('result.md', 'w') as j:
            j.writelines(content)

# def extract_roadmap():

def extract_projectList():
    page = Fetcher.get('https://roadmap.sh/projects')
    # print(page)
    # with open ('roadmap.md', 'w') as f:
    #     f.write(page.html_content)
        # f.write(page.markdown())
    # print("project_list , ", page.html_content.getall("span.my3"))
    # print("project_list , ", page.html_content.getall("span.my3"))
    # page.html_content.getall("span.my3")

    with open('project_list.html', 'w') as f:
        f.write(str(page.markdown()))
        # f.write(str(page.children))
        # f.write(str(page.get_all_text()))
        # f.write(str(page.markdown()))
        # f.write("\n\n\n\n\n\n\n\n")

        # print(page.html_content.find("span"))
        # page.html_content.find("span.my3")
        # f.write(str(page.html_content.getall()

# 
        # f.write(str(page.css("span.my3::text").getall()))

        # f.write(str(page.css("div.::span").getall()))
        # f.write(str(page.css("a.flex::span").getall()))
        # f.write(str(page.css("div.::span").getall()))

        # f.write(str(page.html_content.csgetall("span.my3")))

def clean_projectList_md():
    with open('project_list.md', 'r') as f:
        content = f.readlines()[22]

        # extract text inside ( ) 

         
        with open('project_list_cleaned.md', 'w') as j:
            j.writelines(content)
    
        
def extract_projectList():
    base_url = 'https://roadmap.sh'
    with open('project_list_cleaned.md', 'r') as f:
        content = f.readlines()
        # 
        for i in content:
            page = Fetcher.get(f'{base_url}{i.strip()}')
            with open(f'project_{i.strip().replace("/","_")}.md', 'w') as j:
                j.write(page.markdown())
        # Process the content as needed
        # For example, you might want to extract specific information or format it differently

def clean_project_file():

    # open all the files in the current directory that start with "project_" and end with ".md" and clean them 

    import os
    for filename in os.listdir('.'):
        if filename.startswith('project__') and filename.endswith('.md'):
            with open(filename, 'r+') as f:
                    
                    content = f.readlines()
                    content = content[0:1] + content[12:]  # Keep lines after the 12th line
                            
                    # find "Start building and delete 13 lines after it"
                    for i, line in enumerate(content):
                        if "Start Working" in line:
                            # Delete the next 13 lines after this line
                            del content[i + 1:i + 14]
                            break
                    
                    # Find "Happy Coding and delete everything after it"
                    for i, line in enumerate(content):
                        if "Join the Community" in line:
                            # Delete everything after this line
                            content = content[:i]
                            break
                    # with open('accessible-form-ui.md', 'w') as j:
                    f.seek(0)  # Move the file pointer to the beginning of the file
                    f.truncate()  # Clear the file content
                    f.writelines(content)
    
def checkthis():
    with open('project__projects_accessible-form-ui.md', 'r+') as f:
        content = f.readlines()
        content = content[0:1] + content[12:]  # Keep lines after the 12th line

        # find "Start building and delete 13 lines after it"
        for i, line in enumerate(content):
            if "Start Working" in line:
                # Delete the next 13 lines after this line
                del content[i + 1:i + 14]
                break
        
        # Find "Happy Coding and delete everything after it"
        for i, line in enumerate(content):
            if "Join the Community" in line:
                # Delete everything after this line
                content = content[:i]
                break
        # with open('accessible-form-ui.md', 'w') as j:
        f.seek(0)  # Move the file pointer to the beginning of the file
        f.truncate()  # Clear the file content
        f.writelines(content)


        # content = f.readlines()

        # print(content)
        # for i , line in enumerate(content):
        #     del content[1:12]
        #     del content[11:25]
        #     del content[50:]


        # content = content[0:1] + content[12:20] + content[35:66]
        # print(content)
        # f.writelines(content)
        # print(content)

def main():
    # print("Hello from web-scrape!")
    # fn2()
    # fetch_project_details()
    
    # extract_projectList()
    # clean_projectList_md()
    # extract_projectList()
    # clean_project_md(open('project.markdown', 'r').read())
    # clean_project_md()

    # checkthis()
    clean_project_file()


if __name__ == "__main__":
    main()
