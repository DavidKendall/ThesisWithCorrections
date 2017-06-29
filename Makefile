whereami: whereami.tex thesis.bib
	latex whereami
	bibtex whereami
	latex whereami
	latex whereami
	dvips -Ppdf whereami
	ps2pdf -dCompatibility=1.5 -dPDFSETTINGS=/prepress -dEmbedAllFonts=true whereami.ps
	 

main: main.tex thesis.bib
	latex main
	bibtex main
	latex main
	latex main
	dvips -Ppdf main
	ps2pdf -dCompatibility=1.5 -dPDFSETTINGS=/prepress -dEmbedAllFonts=true main.ps

main_dvips: main.tex thesis.bib
	latex main
	bibtex main
	latex main
	latex main
	dvips -G0 -Ppdf -o main.ps main.dvi
	ps2pdf -dCompatibilityLevel=1.3 -dMaxSubsetPct=100 -dSubsetFonts=true -dEmbedAllFonts=true -dAutoFilterColorImages=false -dAutoFilterGrayImages=false -dColorImageFilter=/FlateEncode -dGrayImageFilter=/FlateEncode -dMonoImageFilter=/FlateEncode main.ps main.pdf

clean:
	for d in . FRONT CHAPTER-1 CHAPTER-2 CHAPTER-3 CHAPTER-4 CHAPTER-5 CHAPTER-6 CHAPTER-7 CHAPTER-8 APPENDIX-1; do \
	    (cd $$d; rm -f *~ *.aux *.bbl *.blg *.dvi *.lof *.log *.lot *.out *.pdf *.ps *.toc) \
	done
