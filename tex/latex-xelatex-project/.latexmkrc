\documentclass[a4paper,12pt]{article}

% Use XeLaTeX
\usepackage{fontspec} % Allows font customization
\usepackage{polyglossia} % For multilingual support
\setdefaultlanguage{english} % Set the default language

% Set the main font (you can change this to any font installed on your system)
\setmainfont{Times New Roman}

% Optional: Set a different font for sans-serif and monospaced text
\setsansfont{Arial}
\setmonofont{Courier New}

\usepackage{graphicx} % For including images
\usepackage{amsmath} % For advanced math typesetting
\usepackage{hyperref} % For hyperlinks

\title{My XeLaTeX Document}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

\section{Introduction}
This is a simple document created using XeLaTeX. You can use various fonts and languages with XeLaTeX.

\section{Including Graphics}
You can include images in your document as follows:
\begin{figure}[h]
    \centering
    \includegraphics[width=0.5\textwidth]{example-image} % Replace with your image file
    \caption{An example image.}
    \label{fig:example}
\end{figure}

\section{Mathematics}
You can also write mathematical equations, such as:
\begin{equation}
    E = mc^2
\end{equation}

\section{Conclusion}
This is a basic template to get you started with XeLaTeX. You can expand upon it by adding more sections, figures, and references.

\end{document}