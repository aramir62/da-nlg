import pandas as pd
import random as rand

das_laptop = ["confirm", "compare", "recommend", "inform", "inform count", "inform all", "inform no match",
              "inform no info", "inform only match", "suggest"]
das_mapping = {"confirm": "confirm", "compare": "compare", "recommend": "describe", "inform": "describe", "inform count":"inform count",
               "inform all": "inform all", "inform no match": "inform no match",
              "inform no info":"inform no info", "inform only match":"inform only match", "suggest":"suggest"}
values_laptop = {"batteryrating": "battery rating",
                 "isforbusinesscomputing": "is for business computing",
                 "pricerange":"price range",
                 "driverange":"drive range", "count":"count", "dontcare":"don't care", "name":"", "hasusbport":"has usb port",
                 "hdmiport":"hdmi port", "screensizerange":"screen size range",
                 'powerconsumption':'power consumption', 'ecorating':"eco rating",
                 "screensize": "screen size", "dont_care":"don't care"}
train_tv = pd.read_json("../../../RNNLG/tv/train.json")
train_laptop = pd.read_json("../../../RNNLG/laptop/train.json")
#valid_laptop = pd.read_json("RNNLG/laptop/valid.json")
test_laptop = pd.read_json("../../../RNNLG/laptop/test.json")
test_tv = pd.read_json("../../../RNNLG/tv/test.json")
def write_priming_samples(filename, priming_header):
    with open(filename, "w") as text_file:
        text_file.write(priming_header)

def tv_test():
    prompts = []

    data_dict = {"orig_mr": [], "da": [], "new_da":[],
                 "pseudo": [], "human_ref": [],
                 "hdc": [], "tst":[]}
    # certaion attributes need to be realized with the name itself
    for n, i in enumerate(test_tv[0]):
        da = i.split("(")[0].replace("?", "").strip().replace("_", " ")
        if da in das_laptop:
            ents = ""
            for m in i.split("(")[1].split(")")[0].split(";"):
                entity_name = m.replace("=", ' ')

                for k, v in values_laptop.items():
                    entity_name = entity_name.replace(k, v)

                ents += entity_name + " "
         #   print(ents)
            ling = "a"
            if da[0] in ["a", "e", "i", "o", "u"]:
                ling = "an"
            new_da = das_mapping[da]
            ents = ents.strip()
            callison_human_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {new_da} dialogue act: "'
          #  callison_hdc_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {da} dialogue act: "'
            prompts.append(callison_human_ref)
           # prompts.append(callison_hdc_ref)
            data_dict["orig_mr"].append(i)
            data_dict["da"].append(da)
            data_dict["new_da"].append(new_da)
            data_dict["pseudo"].append(ents)
            data_dict["human_ref"].append(test_tv[1][n])
            data_dict["hdc"].append(test_tv[2][n])
            data_dict["tst"].append(callison_human_ref)

    pd.DataFrame.from_dict(data_dict).to_csv("10_tv/rnnlg_tv_test.csv")

def tv_pseudos():
    prompts = []
    needed_ent = ["count", "driverange", "is"]
    ents = []
    data_dict = {"orig_mr": [], "da": [], "new_da":[],
                 "pseudo": [], "human_ref": [],
                 "hdc": [], "tst_human":[], "tst_hdc":[]}
    # certaion attributes need to be realized with the name itself
    for n, i in enumerate(train_tv[0]):
        da = i.split("(")[0].replace("?", "").strip().replace("_", " ")
        if da in das_laptop:
            ents = ""
            for m in i.split("(")[1].split(")")[0].split(";"):
                entity_name = m.replace("=", ' ')

                for k, v in values_laptop.items():
                    entity_name = entity_name.replace(k, v)

                ents += entity_name + " "
         #   print(ents)
            ling = "a"
            if da[0] in ["a", "e", "i", "o", "u"]:
                ling = "an"
            ents = ents.strip()
            new_da = das_mapping[da]
            callison_human_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {new_da} dialogue act: "{train_tv[1][n].strip()}"' + "\n"
            callison_hdc_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {new_da} dialogue act: "{train_tv[2][n].strip()}"' + "\n"
            prompts.append(callison_human_ref)
            prompts.append(callison_hdc_ref)
            data_dict["orig_mr"].append(i)
            data_dict["da"].append(da)
            data_dict["new_da"].append(new_da)
            data_dict["pseudo"].append(ents)
            data_dict["human_ref"].append(train_tv[1][n])
            data_dict["hdc"].append(train_tv[2][n])
            data_dict["tst_human"].append(callison_human_ref)
            data_dict["tst_hdc"].append(callison_hdc_ref)
    pd.DataFrame.from_dict(data_dict).to_csv("10_tv/rnnlg_tv_train.csv")

def laptop_pseudos():
    prompts = []
    needed_ent = ["count", "driverange", "is" ]
    ents = []
    data_dict = {"orig_mr": [], "da": [], "new_da": [],
                 "pseudo": [], "human_ref": [],
                 "hdc": [], "tst_human": [], "tst_hdc": []}
    #certaion attributes need to be realized with the name itself
    for n, i in enumerate(train_laptop[0]):
        da = i.split("(")[0].replace("?", "").strip().replace("_", " ")
        if da in das_laptop:
            ents = ""
            for m in i.split("(")[1].split(")")[0].split(";"):
                entity_name = m.replace("=", ' ')

                for k, v in values_laptop.items():
                   entity_name = entity_name.replace(k, v)
                ents += entity_name+" "
           # print(ents)
            ling = "a"
            if da[0] in ["a", "e", "i", "o", "u"]:
                ling = "an"
            ents = ents.strip()
            new_da = das_mapping[da]
            callison_human_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {new_da} dialogue act: "{train_laptop[1][n].strip()}"' + "\n"
            callison_hdc_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {new_da} dialogue act: "{train_laptop[2][n].strip()}"' + "\n"
            prompts.append(callison_human_ref)
            prompts.append(callison_hdc_ref)
            data_dict["orig_mr"].append(i)
            data_dict["da"].append(da)
            data_dict["new_da"].append(new_da)
            data_dict["pseudo"].append(ents)
            data_dict["human_ref"].append(train_laptop[1][n])
            data_dict["hdc"].append(train_laptop[2][n])
            data_dict["tst_human"].append(callison_human_ref)
            data_dict["tst_hdc"].append(callison_hdc_ref)




    pd.DataFrame.from_dict(data_dict).to_csv("10_laptop/rnnlg_laptop_train.csv")


def laptop_test():
    prompts = []

    data_dict = {"orig_mr": [], "da": [], "new_da": [],
                 "pseudo": [], "human_ref": [],
                 "hdc": [], "tst": []}
    # certaion attributes need to be realized with the name itself
    for n, i in enumerate(test_laptop[0]):
        da = i.split("(")[0].replace("?", "").strip().replace("_", " ")
        if da in das_laptop:
            ents = ""
            for m in i.split("(")[1].split(")")[0].split(";"):
                entity_name = m.replace("=", ' ')

                for k, v in values_laptop.items():
                    entity_name = entity_name.replace(k, v)

                ents += entity_name + " "
            #   print(ents)
            ling = "a"
            if da[0] in ["a", "e", "i", "o", "u"]:
                ling = "an"
            ents = ents.strip()
            new_da = das_mapping[da]
            callison_human_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {new_da} dialogue act: "'
            #  callison_hdc_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {da} dialogue act: "'
            prompts.append(callison_human_ref)
            # prompts.append(callison_hdc_ref)
            data_dict["orig_mr"].append(i)
            data_dict["da"].append(da)
            data_dict["new_da"].append(new_da)
            data_dict["pseudo"].append(ents)
            data_dict["human_ref"].append(test_laptop[1][n])
            data_dict["hdc"].append(test_laptop[2][n])
            data_dict["tst"].append(callison_human_ref)

    pd.DataFrame.from_dict(data_dict).to_csv("10_laptop/rnnlg_laptop_test.csv")

tv_pseudos()
laptop_pseudos()

laptop_test()
tv_test()


# values_laptop = {"batteryrating": "battery rating",
#                  "isforbusinesscomputing": "is for business computing",
#                  "pricerange":"price range",
#                  "driverange":"drive range", "count":"count", "dontcare":"don't care", "name":"", "hasusbport":"has usb port",
#                  "hdmiport":"hdmi port", "screensizerange":"screen size range",
#                  'powerconsumption':'power consumption', 'ecorating':"eco rating",
#                  "screensize": "screen size", "kidsallowed":"kids allowed", "goodformeal":"good for meal", "dont_care":"don't care"}
# def train_test(data, das, outfile):
#     prompts = []
#
#     data_dict = {"orig_mr": [], "da": [],
#                  "pseudo": [], "human_ref": [],
#                  "hdc": [], "tst":[]}
#     # certaion attributes need to be realized with the name itself
#     for n, i in enumerate(data[0]):
#         da = i.split("(")[0].replace("?", "").strip().replace("_", " ")
#         if da == "reqmore":
#             da = "request more"
#         ents = ""
#         for m in i.split("(")[1].split(")")[0].split(";"):
#             entity_name = m.replace("=", ' ')
#
#             for k, v in values_laptop.items():
#                 entity_name = entity_name.replace("'","").replace(k, v)
#
#             ents += entity_name + " "
#      #   print(ents)
#         ling = "a"
#         if da[0] in ["a", "e", "i", "o", "u"]:
#             ling = "an"
#         ents = ents.strip()
#         callison_human_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {da} dialogue act: "'
#       #  callison_hdc_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {da} dialogue act: "'
#         prompts.append(callison_human_ref)
#        # prompts.append(callison_hdc_ref)
#         data_dict["orig_mr"].append(i)
#         data_dict["da"].append(da)
#         data_dict["pseudo"].append(ents)
#         data_dict["human_ref"].append(data[1][n])
#         data_dict["hdc"].append(data[2][n])
#         data_dict["tst"].append(callison_human_ref)
#
#     pd.DataFrame.from_dict(data_dict).to_csv(outfile)
#
# def train_pseudos(data, das, outfile):
#     prompts = []
#     needed_ent = ["count", "driverange", "is"]
#     ents = []
#     data_dict = {"orig_mr": [], "da": [],
#                  "pseudo": [], "human_ref": [],
#                  "hdc": [], "tst_human":[], "tst_hdc":[]}
#     # certaion attributes need to be realized with the name itself
#     for n, i in enumerate(data[0]):
#         da = i.split("(")[0].replace("?", "").strip().replace("_", " ")
#         if da == "reqmore":
#             da = "request more"
#         ents = ""
#         for m in i.split("(")[1].split(")")[0].split(";"):
#             entity_name = m.replace("=", ' ')
#
#             for k, v in values_laptop.items():
#                 entity_name = entity_name.replace("'","").replace(k, v)
#
#             ents += entity_name + " "
#      #   print(ents)
#         ling = "a"
#         if da[0] in ["a", "e", "i", "o", "u"]:
#             ling = "an"
#         ents = ents.strip()
#         callison_human_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {da} dialogue act: "{data[1][n].strip()}"' + "\n"
#         callison_hdc_ref = f'Here is a text: "{ents}". Here is a rewrite of the text, which is {ling} {da} dialogue act: "{data[2][n].strip()}"' + "\n"
#         prompts.append(callison_human_ref)
#         prompts.append(callison_hdc_ref)
#         data_dict["orig_mr"].append(i)
#         data_dict["da"].append(da)
#         data_dict["pseudo"].append(ents)
#         data_dict["human_ref"].append(data[1][n])
#         data_dict["hdc"].append(data[2][n])
#         data_dict["tst_human"].append(callison_human_ref)
#         data_dict["tst_hdc"].append(callison_hdc_ref)
#     pd.DataFrame.from_dict(data_dict).to_csv(outfile)
#
#
# das_laptop = ["confirm", "compare", "recommend", "inform", "inform count", "inform all", "inform no match",
#               "inform no info", "inform only match", "suggest", "select"]
# values_laptop = {"batteryrating": "battery rating",
#                  "isforbusinesscomputing": "is for business computing",
#                  "pricerange":"price range",
#                  "driverange":"drive range", "count":"count", "dontcare":"don't care", "name":"", "hasusbport":"has usb port",
#                  "hdmiport":"hdmi port", "screensizerange":"screen size range",
#                  'powerconsumption':'power consumption', 'ecorating':"eco rating",
#                  "screensize": "screen size", "kidsallowed":"kids allowed", "goodformeal":"good for meal", "dont_care":"don't care"}
#
# rest_das = []
#
# hotel_das=[]
# train_restaurant = pd.read_json("../../../RNNLG/restaurant/train.json")
# train_hotel = pd.read_json("../../../RNNLG/hotel/train.json")
# #valid_laptop = pd.read_json("RNNLG/laptop/valid.json")
# test_restaurant = pd.read_json("../../../RNNLG/restaurant/test.json")
# test_hotel = pd.read_json("../../../RNNLG/hotel/test.json")
# train_test(test_restaurant, das_laptop, "10_restaurant/rnnlg_restaurant_test.csv")
# train_test(test_hotel, das_laptop, "10_hotel/rnnlg_hotel_test.csv")
#
# train_pseudos(train_restaurant, das_laptop, "10_restaurant/rnnlg_restaurant_train.csv")
# train_pseudos(train_hotel, das_laptop, "10_hotel/rnnlg_hotel_train.csv")