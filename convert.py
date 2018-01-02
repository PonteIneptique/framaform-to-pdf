from csv import reader
from markdown2 import markdown
from weasyprint import HTML
import glob


stage_i = 0

ignored = list(range(9))

for file in glob.glob("./input/*.tsv"):
    print("Converting " + file)
    with open(file) as file_io:
        csv = reader(file_io, delimiter="\t", quotechar="\"")
        template = ""
        for line_no, line in enumerate(csv):
            if line_no == 0:
                template += line[0] + "\n==="
            elif line_no == 1:
                for colid, column_head in enumerate(line):
                    if colid not in ignored:
                        if column_head:
                            template += "\n## " + column_head + "\n\n### {title_"+\
                                        str(colid)+"} \n {content_"+str(colid)+"}\n"
                        else:
                            template += "\n### {title_"+str(colid)+"} \n {content_"+str(colid)+"}\n"
            elif line_no == 2:
                for title_id, title in enumerate(line):
                    if title_id not in ignored:
                        template = template.replace("{title_"+str(title_id)+"}", title)
            else:
                stage = ""+template
                for colid, column in enumerate(line):
                    if colid not in ignored:
                        stage = stage.replace("{content_" + str(colid) + "}", column)
                html = HTML(string=markdown(stage)).write_pdf("./output/stage_{i}.pdf".format(i=stage_i))
                stage_i += 1
print(str(stage_i) + " files created")
