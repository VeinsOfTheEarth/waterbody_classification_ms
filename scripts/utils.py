import tabulate
import subprocess


def pdf_table(
    dt,    
    path_pdf,
    title=None,
    headers=["Explanatory", "Regressor", "R2", r"Event Percentile"],
    maxcolwidths=None,
    render_only=False,
):

    # if maxcolwidths is None:
    #     maxcolwidths = [1 for _ in range(dt.shape[1])]

    if not render_only:
        mdtable = tabulate.tabulate(
            dt,
            # headers=headers,
            # tablefmt="grid",
            maxcolwidths=maxcolwidths,
            showindex=False,
            numalign="left",
        )
        with open("mdtable.md", "w") as f:
            f.write(mdtable)

        # macos specific commands
        # subprocess.call(
        #     'echo "## ' + title + '\n\n$(cat mdtable.md)" > mdtable.md',
        #     shell=True,
        # )
        subprocess.call(
            'echo "\\pagenumbering{gobble}\n\n$(cat mdtable.md)" > mdtable.md',
            shell=True,
        )
        subprocess.call(
            'echo "---\nheader-includes:\n\t\\usepackage[margin=0.5in]{geometry}\n---\n\n$(cat mdtable.md)" > mdtable.md',
            shell=True,
        )

        # linux specific commands
        # subprocess.call(
        #     "echo ## " + title + "| cat - mdtable.md > temp && mv temp mdtable.md",
        #     shell=True,
        # )
        # subprocess.call(
        #     "echo \\pagenumbering{gobble}| cat - mdtable.md > temp && mv temp mdtable.md",
        #     shell=True,
        # )

    subprocess.call(
        "pandoc --columns=10 mdtable.md -V fontsize=14pt -o " + path_pdf,
        # + " --pdf-engine-opt=-shell-escape",
        shell=True,
    )

    try:  # conda pdfcrop
        subprocess.check_call(
            "pdfcrop.pl " + path_pdf + " " + path_pdf,
            shell=True,
        )
    except:  # system pdfcrop
        try:
            subprocess.call(
                "pdfcrop " + path_pdf + " " + path_pdf,
                shell=True,
            )
        except:
            print("Not able to crop")
            pass