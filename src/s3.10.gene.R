source("functions.R")
diri = glue("{dird}/30_session_templates")

tgl = gcfg$gene %>%
    mutate(b = start - 1100, e = end + 1100) %>%
    mutate(loc = glue("{chrom}:{b}-{e}")) %>%
    select(gid,ttype,loc)

#{{{ cage sessions
opt = 'cage'
fi = glue("{diri}/{opt}.json")
istr = read_file(fi)
#
diro = glue("{dird}/zhoup-igv-data/sessions/{opt}")

ti = read_tsv("~/projects/cage/data/91_share/05.shift.3198.tsv")
glue2 <- function(l, istr) glue(istr, .open = "<<", .close = ">>", locus = l)
to = tgl %>% filter(gid %in% ti$gid) %>%
    mutate(ostr = map(loc, glue2, istr=istr)) %>%
    mutate(fo = glue("{diro}/{gid}.json"))

to %>%# slice(1:10) %>%
    mutate(x = map2(ostr, fo, write_file))
#}}}



