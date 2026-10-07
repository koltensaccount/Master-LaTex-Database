use strict;
use warnings;
our ($out_dir, $aux_dir, $filename);
use Cwd qw(getcwd);
use File::Basename qw(fileparse);
use File::Path qw(make_path);
use File::Spec;

sub _mathnotes_should_redirect_output_from_path {
    my ($abs_path) = @_;
    return 0 if !defined $abs_path || $abs_path eq q{};
    return ($abs_path =~ m{/projects/(lecture|discussion|homework|reports)/}
          || $abs_path =~ m{/projects/textbook/src/});
}

sub _mathnotes_target_dir_from_tex {
    my ($abs_path) = @_;
    my ($basename, $dir) = fileparse($abs_path, qr/\.[^.]*/);
    return if $basename eq q{};

    my $subdir = File::Spec->catdir($dir, $basename);
    return File::Spec->canonpath($subdir);
}

{
    no warnings 'redefine';
    *mathnotes_orig_normalize_aux_out_ETC = \&normalize_aux_out_ETC;
    *normalize_aux_out_ETC = sub {
        if ( (!$out_dir || $out_dir eq '.') && defined $filename ) {
            my $abs_path = File::Spec->rel2abs($filename, getcwd());
            if ( _mathnotes_should_redirect_output_from_path($abs_path) ) {
                my $target_dir = _mathnotes_target_dir_from_tex($abs_path);
                if ($target_dir) {
                    if ( !-d $target_dir ) {
                        make_path($target_dir)
                          or die "latexmk: unable to create standalone output directory '$target_dir'";
                    }
                    $out_dir = $target_dir;
                    $aux_dir = $target_dir;
                }
            }
        }
        goto &mathnotes_orig_normalize_aux_out_ETC;
    };
}

1;
