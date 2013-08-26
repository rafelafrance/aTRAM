use strict;

my $fastafile_1 = shift;
my $fastafile_2 = shift;
my $seq_blast = shift;

my $seq_names = "$seq_blast.sorted";
my $outfile = "$seq_names.fasta";
system ("gawk '{sub(\"/1\",\"\");print \$2;}' $seq_blast | sort | uniq -u > $seq_names");
# print "made file $seq_names\n";

open LIST_FH, "<", "$seq_names";
open FA1_FH, "<", "$fastafile_1";
open FA2_FH, "<", "$fastafile_2";
open OUT_FH, ">", "$outfile";

my $curr_name = readline LIST_FH;

while ($curr_name) {
	chomp $curr_name;
	my $fa_seq1 = (readline FA1_FH) . (readline FA1_FH);
	my $fa_seq2 = (readline FA2_FH) . (readline FA2_FH);

	if ($fa_seq1 eq "") { last; }
	if ($fa_seq2 eq "") { last; }

	if ($fa_seq1 =~ /$curr_name/) {
# 		print "found $curr_name\n";
		print OUT_FH "$fa_seq1$fa_seq2";
		$curr_name = readline LIST_FH;
	}
}

close LIST_FH;
close FA1_FH;
close FA2_FH;
close OUT_FH;
