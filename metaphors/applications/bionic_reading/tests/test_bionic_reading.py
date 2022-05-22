import unittest

from metaphors.applications.bionic_reading.features.bionic_reading import BionicReading


class TestBionicReading(unittest.TestCase):
    def test_html_correct(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "<!DOCTYPE html><html><head><style>b {font-weight: 700}</style></head><body><p><b>W</b>e <b>ar</b>e <b>hap</b>py <b>i</b>f <b>a</b>s <b>ma</b>ny <b>peop</b>le <b>a</b>s <b>possi</b>ble <b>ca</b>n <b>us</b>e <b>th</b>e <b>advan</b>tage <b>o</b>f <b>Bion</b>ic <b>Readi</b>ng.</p></body></html>"
        self.assertTrue(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7).read_faster(text=text, output_format="html")
            == expected_output
        )

    def test_python_correct(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "\x1b[1mW\x1b[0me \x1b[1mar\x1b[0me \x1b[1mhap\x1b[0mpy \x1b[1mi\x1b[0mf \x1b[1ma\x1b[0ms \x1b[1mma\x1b[0mny \x1b[1mpeop\x1b[0mle \x1b[1ma\x1b[0ms \x1b[1mpossi\x1b[0mble \x1b[1mca\x1b[0mn \x1b[1mus\x1b[0me \x1b[1mth\x1b[0me \x1b[1madvan\x1b[0mtage \x1b[1mo\x1b[0mf \x1b[1mBion\x1b[0mic \x1b[1mReadi\x1b[0mng."
        self.assertTrue(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7).read_faster(text=text, output_format="python")
            == expected_output
        )

    def test_html_incorrect(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "<!DOCTYPE html><html><head><style>b {font-weight: 700}</style></head><body><p><b>W</b>e <b>ar</b>e <b>hap</b>py <b>i</b>f <b>a</b>s <b>ma</b>ny <b>peop</b>le <b>a</b>s <b>possi</b>ble <b>ca</b>n <b>us</b>e <b>th</b>e <b>advan</b>tage <b>o</b>f <b>Bion</b>ic <b>Readi</b>ng.</p></body></html>"
        self.assertFalse(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7).read_faster(text=text, output_format="python")
            == expected_output
        )

    def test_python_incorrect(self):
        text = "We are happy if as many people as possible can use the advantage of Bionic Reading."
        expected_output = "\x1b[1mW\x1b[0me \x1b[1mar\x1b[0me \x1b[1mhap\x1b[0mpy \x1b[1mi\x1b[0mf \x1b[1ma\x1b[0ms \x1b[1mma\x1b[0mny \x1b[1mpeop\x1b[0mle \x1b[1ma\x1b[0ms \x1b[1mpossi\x1b[0mble \x1b[1mca\x1b[0mn \x1b[1mus\x1b[0me \x1b[1mth\x1b[0me \x1b[1madvan\x1b[0mtage \x1b[1mo\x1b[0mf \x1b[1mBion\x1b[0mic \x1b[1mReadi\x1b[0mng."
        self.assertFalse(
            BionicReading(fixation=0.6, saccades=0.75, opacity=0.7).read_faster(text=text, output_format="html")
            == expected_output
        )
