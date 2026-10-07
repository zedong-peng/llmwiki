% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A new style for DatabricksAI pre-prints
% Author: mosaic-research-team@databricks.com
% Version: 1.1
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Class declarations %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{databricksai}
\LoadClassWithOptions{article}

% Layout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage[top=2.25cm, bottom=2.5cm, left=2.5cm, right=2.5cm, columnsep=0.65cm]{geometry}
\RequirePackage[tracking=smallcaps]{microtype}
\RequirePackage{placeins}
\RequirePackage{hyphenat}
\RequirePackage{setspace}
\RequirePackage{parskip}
\RequirePackage[latin, english]{babel}
\RequirePackage{lipsum}
\RequirePackage{etoolbox}
\RequirePackage{fancyhdr}

\DisableLigatures[f]{family=sf*} 

% Graphics %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{graphicx}
\RequirePackage{subcaption}

% Tables %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{booktabs}
\RequirePackage{nicematrix}
\RequirePackage{multirow}
\RequirePackage{bm}
\newcommand{\nm}[1]{#1}

% Colorful stuff %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage[most]{tcolorbox}
\RequirePackage{xcolor}
\definecolor{dbxblue}{HTML}{0064E0}
\definecolor{dbxred}{HTML}{FF3621}
\definecolor{dbxfg}{HTML}{1C2B33}
\definecolor{dbxbg}{HTML}{F1F4F7}

% References %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{hyperref}
\RequirePackage[noabbrev,nameinlink]{cleveref}
\hypersetup{
  colorlinks,
  linkcolor=dbxred,
  citecolor=dbxblue,
  urlcolor=dbxred
}

\RequirePackage[round,authoryear]{natbib}
\def\bibfont{\small}

% Font styling: DMSans for display; default LaTeX serif for body.
\newcommand{\metadisplayfont}{\fontfamily{dmsans}\selectfont}
\newcommand{\runningtitle}{}
\newcommand{\firstpagefootertext}{}
\newcommand{\runningfootertext}{}
\newcommand{\setfirstpagefooter}[1]{\gdef\firstpagefootertext{#1}}
\newcommand{\setrunningfooter}[1]{\gdef\runningfootertext{#1}}
% Backward compatibility: set footer text for pages 2+ only.
\newcommand{\setglobalfooter}[1]{\setrunningfooter{#1}}
\newcommand{\copyrightnotice}{\copyright\ \the\year\ Databricks. All rights reserved}
\newcommand{\setcopyrightnotice}[1]{\gdef\copyrightnotice{#1}}

% Footer styling via fancyhdr
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% Header behavior: no header on first page; centered running title from page 2 onward.
\newcommand{\stripnewlines}[1]{%
  \begingroup
  \renewcommand{\\}{ }% Replaces \\ with a space
  #1%
  \endgroup
}
\fancyhead[L]{}
\fancyhead[C]{\small\metadisplayfont\mdseries \stripnewlines{\runningtitle} - Databricks AI Research}
\fancyhead[R]{}

% Two-line footer on all pages; page 1 additionally shows the copyright notice.
\newcommand{\dbxfooterblock}[2]{%
  \vspace{5pt}
  \hrule height 0.4pt width \textwidth
  \vspace{2pt}
  {\small\metadisplayfont\mdseries
    \parbox[t]{\textwidth}{%
      \ifstrempty{#1}{\strut}{#1}\par
      #2%
    }%
  }%
}

\fancyfoot[C]{}
\fancyfoot[R]{}
\fancyfoot[L]{%
  \vspace{5pt}
  \hrule height 0.4pt width \textwidth
  \vspace{2pt}
  {\small\metadisplayfont\mdseries
    \ifstrempty{\runningfootertext}{}{\runningfootertext\hspace{0.75em}}\hfill \thepage
  }
}

\fancypagestyle{firststyle}{
  \fancyhf{}
  \fancyhead[L]{}
  \fancyhead[C]{}
  \fancyhead[R]{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyfoot[C]{}
  \fancyfoot[R]{}
  \fancyfoot[L]{%
    \dbxfooterblock{\firstpagefootertext}{\copyrightnotice\hfill \thepage}%
  }
}

% Section and caption format %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\RequirePackage{titlesec}
% \titleformat*{\paragraph}{\itshape} % JACK CHANGED 0902
\titleformat*{\paragraph}{\metadisplayfont\bfseries}
\titleformat*{\section}{\Large\metadisplayfont\bfseries}
\titleformat*{\subsection}{\large\metadisplayfont\bfseries}
\titleformat*{\subsubsection}{\normalsize\metadisplayfont\bfseries}
\DeclareTextFontCommand{\textbf}{\bfseries}

\RequirePackage{caption}
\DeclareCaptionLabelSeparator{custom}{}
\DeclareCaptionFormat{custom}{{\metadisplayfont\textbf{#1 #2}} #3}
\captionsetup{singlelinecheck=false,format=custom,labelsep=custom,font=small}
\captionsetup[sub]{singlelinecheck=true,format=custom,labelsep=custom,font=small}

% DatabricksAI custom fonts %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% \renewcommand*\ttdefault{cmvtt}
\RequirePackage[T1]{fontenc}
\RequirePackage{amsmath,amsfonts,amssymb}

\renewcommand{\familydefault}{\rmdefault}


\DeclareFontFamily{T1}{dmsans}{}
\DeclareFontShape{T1}{dmsans}{m}{n}{<-> s * [0.88] DMS-Regular--base}{}
\DeclareFontShape{T1}{dmsans}{m}{it}{<-> s * [0.88] DMS-Italic--base}{}
\DeclareFontShape{T1}{dmsans}{m}{sl}{<-> s * [0.88] DMS-Italic--base}{}
\DeclareFontShape{T1}{dmsans}{b}{n}{<-> s * [0.88] DMS-Bold--base}{}
\DeclareFontShape{T1}{dmsans}{b}{it}{<-> s * [0.88] DMS-BoldItalic--base}{}
\DeclareFontShape{T1}{dmsans}{b}{sl}{<-> s * [0.88] DMS-BoldItalic--base}{}
\DeclareFontShape{T1}{dmsans}{bx}{n}{<-> s * [0.88] DMS-Bold--base}{}
\DeclareFontShape{T1}{dmsans}{bx}{it}{<-> s * [0.88] DMS-BoldItalic--base}{}
\DeclareFontShape{T1}{dmsans}{bx}{sl}{<-> s * [0.88] DMS-BoldItalic--base}{}
\pdfmapline{+DMS-Regular--base DMSans-Regular "AutoEnc_xl5cmsgoc2zisarxhqlxvc7v4c ReEncodeFont" <[a_xl5cms.enc <dm-sans-regular.ttf}
\pdfmapline{+DMS-Italic--base DMSans-Italic "AutoEnc_xl5cmsgoc2zisarxhqlxvc7v4c ReEncodeFont" <[a_xl5cms.enc <dm-sans-italic.ttf}
\pdfmapline{+DMS-Bold--base DMSans-Bold "AutoEnc_xl5cmsgoc2zisarxhqlxvc7v4c ReEncodeFont" <[a_xl5cms.enc <dm-sans-bold.ttf}
\pdfmapline{+DMS-BoldItalic--base DMSans-BoldItalic "AutoEnc_xl5cmsgoc2zisarxhqlxvc7v4c ReEncodeFont" <[a_xl5cms.enc <dm-sans-bold-italic.ttf}
\renewcommand{\sfdefault}{dmsans}

% Authors, affiliations, infos %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand\addtolist[5][]{
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect 
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}

\newcommand\authorlist{}
\newcommand\authorformat[2][]{{\metadisplayfont \bfseries #2$^{#1}$}}
\renewcommand\author[2][]{\addtolist[#1]{#2}{\authorlist}{\authorformat}{, }}

\newcommand\affiliationlist{}
\newcommand\affiliationformat[2][]{{\normalsize $^{#1}$#2}}
\newcommand\affiliation[2][]{\addtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand\contributionlist{}
\newcommand\contributionformat[2][]{{\small $^{#1}$#2}}
\newcommand\contribution[2][]{\addtolist[#1]{#2}{\contributionlist}{\contributionformat}{, }}

\newcommand\metadatalist{}
\newcommand\metadataformat[2][]{{\small {\metadisplayfont \bfseries #1:} #2}}
\newcommand\metadata[2][]{\addtolist[#1]{#2}{\metadatalist}{\metadataformat}{\par}}

\renewcommand{\abstract}[1]{\def\abstractlist{{\color{dbxfg} #1}}}
\newcommand{\email}[1]{\href{mailto:#1}{\texttt{#1}}}

\renewcommand\date[1]{\metadata[Date]{#1}}
\newcommand\correspondence[1]{\metadata[Correspondence]{#1}}

\renewcommand{\title}[1]{%
  \gdef\runningtitle{#1}%
  \gdef\titlelist{{\huge\metadisplayfont\bfseries #1}}%
}

\newcommand{\beginappendix}{\appendix{\huge\metadisplayfont Appendix\par}}

% Titlebox %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


\newcommand{\mymaketitle}{%
  \tcbset{enhanced,frame hidden}
  \tcbset{left=0.5cm}
  \tcbset{right=0.5cm}
  \tcbset{top=0.5cm}
  \tcbset{bottom=0.5cm}
  \tcbset{arc=10pt}
  \tcbset{colback=dbxbg}
  \tcbset{before skip=0pt}
  \tcbset{grow to left by=1.5pt}
  \tcbset{grow to right by=1.5pt}
  \tcbset{overlay={\node[
    anchor=south east,
    at= (frame.south east),
    xshift=-0.5cm,
    yshift=0.5cm] {\includegraphics[width=2.8cm]{databricks-logo.eps}};}}
  % 
  \begin{tcolorbox}
    \setlength{\parindent}{0cm}
    \setlength{\parskip}{0.5cm}
    {
      \setlength{\parskip}{0cm}
      \raggedright
      \nohyphens
      %
      {
        \setstretch{1.618}
        \titlelist\par
      }
      \vskip 0.2cm
      %
      \authorlist\par
      \vskip 0.2cm
      %
      \affiliationlist\par
      %
      \contributionlist\par
    }
    %
    \abstractlist\par
    %
    \vskip 0.5cm
    %
    {
      \setlength{\parskip}{0cm}
      \ifdefempty{\metadatalist}{\vspace*{0.65cm}}{\metadatalist\par}
    }
  \end{tcolorbox}
  \tcbset{reset}
  \FloatBarrier
}

\if@twocolumn%
\renewcommand{\maketitle}{
\twocolumn[%
  \mymaketitle
  \vskip 0.38cm
]
\thispagestyle{firststyle}
}%
\else%
\renewcommand{\maketitle}{
  \mymaketitle
  \thispagestyle{firststyle}
}%
\fi
