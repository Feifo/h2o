import unittest, time, sys, time, random
sys.path.extend(['.','..','../..','py'])
import h2o, h2o_cmd, h2o_hosts, h2o_browse as h2b, h2o_import as h2i, h2o_common

DO_RANDOM_SAMPLE = True
print "Assumes you ran ../build_for_clone.py in this directory"
print "Using h2o-nodes.json. Also the sandbox dir"

class releaseTest(h2o_common.ReleaseCommon, unittest.TestCase):

    def test_c6_maprfs(self):
        print "\nLoad a list of files from HDFS, parse and do 1 RF tree"
        print "\nYou can try running as hduser/hduser if fail"
        # larger set in my local dir
        # fails because classes aren't integers
        #    "allstate_claim_prediction_train_set.zip",
        csvFilenameAll = [
            # "3G_poker_shuffle",
            "TEST-poker1000.csv",
            "and-testing.data",
            "arcene2_train.both",
            "arcene_train.both",
            "bestbuy_test.csv",
            "bestbuy_train.csv",
            # "billion_rows.csv.gz",
            "covtype.13x.data",
            "covtype.13x.shuffle.data",
            # "covtype.169x.data",
            "covtype.4x.shuffle.data",
            "covtype.data",
            "covtype4x.shuffle.data",
            "hhp.unbalanced.012.1x11.data.gz",
            "hhp.unbalanced.012.data.gz",
            "hhp.unbalanced.data.gz",
            "hhp2.os.noisy.0_1.data",
            "hhp2.os.noisy.9_4.data",
            "hhp_9_14_12.data",
            "leads.csv",
            "prostate_long_1G.csv",
        ]

        # find_cloud.py won't set these correctly. Let's just set them here
        h2o.nodes[0].use_maprfs = True
        h2o.nodes[0].use_hdfs = False
        h2o.nodes[0].hdfs_version = 'mapr2.1.3',
        h2o.nodes[0].hdfs_name_node = 'mr-0x1.0xdata.loc:7222'

        # pick 8 randomly!
        if DO_RANDOM_SAMPLE:
            csvFilenameList = random.sample(csvFilenameAll,8)
        # Alternatively: do the list in order! Note the order is easy to hard
        else:
            csvFilenameList = csvFilenameAll

        # pop open a browser on the cloud
        # h2b.browseTheCloud()

        # save the first, for all comparisions, to avoid slow drift with each iteration
        for csvFilename in csvFilenameList:
            # creates csvFilename.hex from file in hdfs dir 
            csvPathname = importFolderPath + "/" + csvFilename
            print "Loading", csvFilename, 'from maprfs'
            parseResult = h2i.import_parse(path=csvPathname, schema="maprfs", timeoutSecs=1000)
            print csvFilename, 'parse time:', parseResult['response']['time']
            print "parse result:", parseResult['destination_key']

            print "\n" + csvFilename
            start = time.time()
            RFview = h2o_cmd.runRF(trees=1,parseResult=parseResult,timeoutSecs=2000)
            # h2b.browseJsonHistoryAsUrlLastMatch("RFView")

if __name__ == '__main__':
    h2o.unit_main()
