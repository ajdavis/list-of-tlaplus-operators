import csv
import os
import subprocess
import sys

# Each tuple is (TLA+, LaTeX, TLA+ ASCII representation, description)
symbols = [
    # "Specifying Systems", Table 8: ascii representations of typeset symbols
    (r"\land", r"\land", r"/\ or \land", r"and, conjunction"),
    (r"\lor", r"\lor", r"\/ or \lor", r"or, disjunction"),
    (r"{\lnot}", r"{\lnot}", r"~ or \lnot or \neg", r"not"),
    (r"\in", r"\in", r"\in", r"in"),
    (r"\notin", r"\notin", r"\notin", r"not in"),
    (r"{\langle}x, y{\rangle}", r"{\langle}x, y{\rangle}", r"<< x, y>>",
     r"a tuple containing some x, y"),
    (r"<", r"<", r"<", r"less than"),
    (r"\leq", r"\leq", r"\leq or =<", r"less than or equal"),
    (r"\ll", r"\ll", r"\ll", r"much less?"),
    (r"\equiv", r"\equiv", r"<=> or \equiv", r"is equivalent to"),
    (r">", r">", r">", r"greater"),
    (r"\geq", r"\geq", r"\geq or >=", r"greater or equal"),
    (r"\gg", r"\gg", r"\gg", r"much greater?"),
    (r"\prec", r"\prec", r"\prec", r"precedes"),
    (r"\preceq", r"\preceq", r"\preceq", r"precedes or equals"),
    (r"\succ", r"\succ", r"\succ", r"succeeds"),
    (r"\succeq", r"\succeq", r"\succeq", r"succeeds or equals"),
    (r"\subset", r"\subset", r"\subset", r"subset"),
    (r"\subseteq", r"\subseteq", r"\subseteq", r"subset or equal"),
    (r"\sqsubset", r"\sqsubset", r"\sqsubset", r"bag subset/is a refinement?"),
    (r"\sqsubseteq", r"\sqsubseteq", r"\sqsubseteq",
     r"bag subset or equal/is a refinement or equal?"),
    (r"A \vdash B", r"A \vdash B", r"|-", r"B can be derived from A?"),
    (r"\models", r"\models", r"|=", r"satisfies/models a temporal formula"),
    (r"\rightarrow", r"\rightarrow", r"->", r"set of functions/step"),
    (r"\cap", r"\cap", r"\cap or \intersect", r"intersection"),
    (r"\sqcap", r"\sqcap", r"\sqcap", r""),
    (r"\oplus", r"\oplus", r"(+) or \oplus", r"bag union"),
    (r"\ominus", r"\ominus", r"(-) or \ominus", r"bag difference"),
    (r"\odot", r"\odot", r"(.) or \odot", r""),
    (r"\otimes", r"\otimes", r"(\X) \otimes", r"Cartesian product"),
    (r"\oslash", r"\oslash", r"(/) or \oslash", r""),
    (r"\E", r"\exists", r"\E", r"there exists"),
    (r"\exists!", r"\exists!", r"\exists!", r"there exists exactly one"),
    (r"{\EE}",
     r"\makebox{$\raisebox{.05em}{\makebox[0pt][l]{$\exists\hspace{-.517em}\exists\hspace{-.517em}\exists$}}\exists\hspace{-.517em}\exists\hspace{-.517em}\exists\,$}",
     r"\EE",
     r"temporal existential quantification, 'hiding'"),
    (r"[A]_{ v}", r"[A]_{ v}", r"[A]_v", r"action operator, 'square A sub v'"),
    (r"{\WF}_{ v}", r"WF_{v}", r"WF_v", r"weak fairness variables"),
    (r"{\SF}_{ v}", r"SF_{v}", r"SF_v", r"strong fairness variables"),
    (r"\supseteq", r"\supseteq", r"\supseteq", r"superset"),
    (r"\supset", r"\supset", r"\supset", r"superset or equals"),
    (r"\sqsupset", r"\sqsupset", r"\sqsupset", r"bag superset"),
    (r"\sqsupseteq", r"\sqsupseteq", r"\sqsupseteq", r"bag superset or equal"),
    (r"\dashv", r"\dashv", r"-|", r""),
    (r"\eqdash", r"\eqdash", r"=|", r""),
    (r"\leftarrow", r"\leftarrow", r"<-", r"substitution"),
    (r"\cup", r"\cup", r"\cup or \union", r"union"),
    (r"\sqcup", r"\sqcup", r"\sqcup", r""),
    (r"\uplus", r"\uplus", r"\uplus", r""),
    (r"\times", r"\times", r"\X or \times", r"multiply"),
    (r"\wr", r"\wr", r"\wr", r""),
    (r"\propto", r"\propto", r"\propto", r"propositional something?"),
    (r"\A", r"\forall", r"\A", r"for all"),
    (r"{\AA}",
     r"\makebox{$\raisebox{.05em}{\makebox[0pt][l]{$\forall\hspace{-.517em}\forall\hspace{-.517em}\forall$}}\forall\hspace{-.517em}\forall \hspace{-.517em}\forall\,$}",
     r"\AA", r"temporal universal quantification"),
    (r"{\langle}A{\rangle}_{ v}", r"{\langle}A{\rangle}_{ v}", r"<<A>>_v",
     r"action operator, 'angle A sub v', TODO"),
    (r"\implies", r"\implies", r"=>", r"implies"),
    (r"\defeq", r"\;\mathrel{\smash{{\stackrel{\scriptscriptstyle\Delta}{=}}}}\;", r"==", r"is equivalent"),
    (r"\neq", r"\neq", r"\div", r"not equal?"),
    (r"{\Box}", r"{\Box}", r"[]", r"always in the future/henceforth"),
    (r"{\Diamond}", r"{\Diamond}", r"<>",
     r"sometime(s) in the future/eventually"),

    # From "Specifying Systems" index, not in Table 8
    (r"\leadsto", r"\leadsto", r"~>", r"leads to"),
    (r"E \whileop M", r"E \stackrel{\mbox{\raisebox{-.3em}[0pt][0pt]{$\scriptscriptstyle+\;\,$}}}{-\hspace{-.16em}\triangleright} M", r"-+->",
     r"M remains true at least one step longer than E does"),
    (r"\mapsto", r"\mapsto", r"|->", r"function/record constructor"),
    (r"\div", r"\div", r"\div", r"integer division"),
    (r"\cdot", r"\cdot", r"\cdot", r"composition of actions"),
    (r"\circ", r"\circ", r"\o or \circ", r"concatenate sequences"),
    (r"\bullet", r"\bullet", r"\doteq", r""),
    (r"\star", r"\star", r"\star", r""),
    (r"\bigcirc", r"\bigcirc", r"\bigcirc", r""),
    (r"\sim", r"\sim", r"\sim", r"stuttering equivalent"),
    (r"\simeq", r"\simeq", r"\sim", r"stuttering equivalent"),
    (r"\asymp", r"\asymp", r"\asymp", r""),
    (r"\approx", r"\approx", r"\approx", r""),
    (r"\cong", r"\cong", r"\cong", r""),
    (r"\doteq", r"\doteq", r"\doteq", r""),
    (r"x ^{ y}", r"x ^{ y}", r"x\^{}y", r"exponentiation"),
    (r"'", r"'", r"'", r"prime"),
    (r"\sim", r"\sim", r"\sim", r"stuttering equivalent"),
    (r"!", r"!", r"!", r"new record (in EXCEPT expression)"),
    (r"@", r"@", r"@", r"previous record field value (in EXCEPT expression)"),
    (r":>", r":>", r":>", r"TLC module explicit function operator"),
    (r"@@", r"@@", r"@@", r"TLC module explicit function operator"),

    # Greek, and most variants but not the rarely-used ones.
    (r"\alpha", r"\alpha", r"\alpha", "alpha"),
    (r"\beta", r"\beta", r"\beta", "beta"),
    (r"\gamma", r"\gamma", r"\gamma", "gamma"),
    (r"\Gamma", r"\Gamma", r"\Gamma", "Gamma"),
    (r"\delta", r"\delta", r"\delta", "delta"),
    (r"\Delta", r"\Delta", r"\Delta", "Delta"),
    (r"\epsilon", r"\epsilon", r"\epsilon", "epsilon"),
    (r"\varepsilon", r"\varepsilon", r"\varepsilon", "variant epsilon"),
    (r"\zeta", r"\zeta", r"\zeta", "zeta"),
    (r"\eta", r"\eta", r"\eta", "eta"),
    (r"\theta", r"\theta", r"\theta", "theta"),
    (r"\vartheta", r"\vartheta", r"\vartheta", "variant theta"),
    (r"\Theta", r"\Theta", r"\Theta", "Theta"),
    (r"\iota", r"\iota", r"\iota", "iota"),
    (r"\kappa", r"\kappa", r"\kappa", "kappa"),
    (r"\lambda", r"\lambda", r"\lambda", "lambda"),
    (r"\Lambda", r"\Lambda", r"\Lambda", "Lambda"),
    (r"\mu", r"\mu", r"\mu", "mu"),
    (r"\nu", r"\nu", r"\nu", "nu"),
    (r"o", r"o", r"o", "omicron"),
    (r"\pi", r"\pi", r"\pi", "pi"),
    (r"\Pi", r"\Pi", r"\Pi", "Pi"),
    (r"\rho", r"\rho", r"\rho", "rho"),
    (r"\varrho", r"\varrho", r"\varrho", "variant rho"),
    (r"\sigma", r"\sigma", r"\sigma", "sigma"),
    (r"\varsigma", r"\varsigma", r"\varsigma", "variant sigma"),
    (r"\Sigma", r"\Sigma", r"\Sigma", "Sigma"),
    (r"\tau", r"\tau", r"\tau", "tau"),
    (r"\upsilon", r"\upsilon", r"\upsilon", "upsilon"),
    (r"\Upsilon", r"\Upsilon", r"\Upsilon", "Upsilon"),
    (r"\phi", r"\phi", r"\phi", "phi"),
    (r"\varphi", r"\varphi", r"\varphi", "variant phi"),
    (r"\Phi", r"\Phi", r"\Phi", "Phi"),
    (r"\chi", r"\chi", r"\chi", "chi"),
    (r"\psi", r"\psi", r"\psi", "psi"),
    (r"\Psi", r"\Psi", r"\Psi", "Psi"),
    (r"\omega", r"\omega", r"\omega", "omega"),
    (r"\Omega", r"\Omega", r"\Omega", "Omega"),

    # The Great, Big List of LATEX Symbols
    # https://www.rpi.edu/dept/arc/training/latex/LaTeX_symbols.pdf
    (r"\partial", r"\partial", r"\partial", "partial")
]

print(f'{len(symbols)} symbols')

filename_base = 'all-operators'


def generate_pdf():
    tex_file_name = f'{filename_base}.tex'
    pdf_file_name = f'{filename_base}.pdf'
    log_file_name = f'{filename_base}.log'
    preamble_file_name = f'{filename_base}-preamble.tex'

    f = open(tex_file_name, 'w')
    f.write(open(preamble_file_name).read())

    def writeline(s):
        f.write(s)
        f.write('\n')

    writeline(r'\begin{tabular}{ |c|c|c }')

    for i, (tla_plus, latex, plain, description) in enumerate(symbols):
        escaped = plain.replace('\\', r'$\backslash$')
        escaped = escaped.replace('_', r'\_')
        escaped = escaped.replace('<', r'{\textless}')
        escaped = escaped.replace('>', r'{\textgreater}')
        escaped = escaped.replace('|', r'{\textbar}')
        escaped = escaped.replace('^', r'{\textasciicircum}')
        writeline(r'''\@x{ \.{%s} } &
    \@y{ %s } &
    %s \\
    ''' % (tla_plus, escaped, description))

        if i > 0 and i % 50 == 0:
            writeline(r'\end{tabular}')
            writeline(r'\newpage')
            writeline(r'\begin{tabular}{ |c|c|c }')

    writeline(r'\end{tabular}')
    writeline(r'\end{document}')
    f.close()

    if os.path.exists(pdf_file_name):
        os.remove(pdf_file_name)

    rv = subprocess.call(['pdflatex', tex_file_name])
    if rv == 0:
        print(f"Generated {pdf_file_name}")
    else:
        print(f"pdflatex exited with code {rv}. Read {log_file_name}")

    return rv


def generate_csv():
    csv_file_name = f'{filename_base}.csv'
    writer = csv.writer(open(csv_file_name, 'w'), quoting=csv.QUOTE_ALL)
    for tla_plus, latex, plain, description in symbols:
        writer.writerow((rf"[$$]{latex}[/$$]", plain, description))

    print(f"Generated {csv_file_name}")
    return 0


for fn in generate_pdf, generate_csv:
    fn_return_val = fn()
    if fn_return_val != 0:
        sys.exit(fn_return_val)
