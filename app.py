import os
import sys
import matplotlib
matplotlib.use('Agg')
from flask import Flask, request, flash, render_template
import dalton_method
import signal_fading_sim

import jinja2
loader = jinja2.FileSystemLoader('/tmp')
environment = jinja2.Environment()

UPLOAD_FOLDER = '/home/jpucilos/flask_website/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 0.5 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def divide(dividend, divisor):
    if divisor == 0:
        return 0
    return dividend/divisor

environment.filters['divide'] = divide

photo_urls = ["https://lh3.googleusercontent.com/6whrVMD8sZwtYhrZM6MD11umMFNp7dnJA7T8SpQggStWHSBWfewwabQJMP9OytqQKapo3wac3qvdKWJu80f_yVhHSZkTtpUYfnGCLf2v_6eCRcd-QZQXBgUp9tXpVrHBsO8bCnv7Iy_JwHrUYrhYOlzclZjI2vDcYi-4sCKP8ShM4RiKr5DcWy2jqtVfy0ninrIS8LHwDbsJzXvZkjSPnfvYHpGAMK4hmaBup0n4_oXnqextKuEpYB0BKK4f7T9Ibd4PzpdJOeV5hnyoYLBk_fKosSYNwFR_guccBPmBwTKIumyG5C_PIwGZqU2KVCDgZXlEFw029rusW-D_1vavtF2x0vXZ3J6I7vgOIzHKCUfxSvQr_vaMQXAGKrNNeKcQhehqrl4n1csyJbpwBWwFV8kWTYbyRiKGsz4nlA3dqHnC5P9ybvM07PtIZIS5GMidNjSrKbNSHXP72yRZdqD8_DhrSOTcucIq8U6FOFtxCdk5o-V6ifZrFrHuaz_kSqu8-OpUjqfgoe5FQah0vsupiBWYTp4U02tGirLrVmmdxfBVQHCvo-fLdDuR_C5Z_8gpe9enGC6CcHYq1sewti7y48eljIhsWSxsdu5JovEXg8qiZdPHzwGpN7ygp0MTbHy_dD42vp0h7jXarWeGX4F0pnJ3sccqd8YkJ68kMzjhgM7eBF2auo08BffMpz-ncOIZ2XWvs4JnfHg1CP2Ue-B-xw45DC7wkpa8pw1gnXyJ6XPU2uIlkQ=w1147-h764-no",
"https://lh3.googleusercontent.com/4IPzpFTNLUOJfxkp68nkZEDJC9ly3yY8D7ye4OpDBHLhxt68q3EPbkEAIKxVpRIquNialRgdpRZiXNID4C5Gky3cGzB1URQ4hz4rAs1koqotyAQoT8eMyTAYBhjz5lwReDgrCO5FnBS-p-0M5SZkxhPhIasdaQMN7fHoNonJXJZ5aVhHqf6DBp1sLx38XH5ji2w8DDWpBr3YwamaH26VdDC4IO_B6WSZexKNUjWILrS2ya20hr_2TPTbJDeCqfnZMMryvo3vd0DHlWCJgBqHkVsO4Pa_RTissh2nlcl73-hA3CJV4W62x4C-faxdmspPZVcYf5KbMjOMQKFCcYjW9pr37Cfin56ROkRZaOPywl5Z-Ind7EML2KPMkEihBGRSl_W3sA9WeNKq6bxoFypWu3Bif0GDOu4-nN3-7b2cEQO6VUf9NEOz4NK0xDiW1HyvPqtiHKHC9tOH18FxO2lhoBgWWRJkwAJabXLqp6dHtCrG75jJuw6smoxx_8aNcn4Ci1tsHH0X6h6V45g21K2MYBMJWBemU4nUZQthtEiW5SJYp97dV6aY5NzjB0wnK7xyaRU8NNBnJC5SGLjySihNA0C5WMInymQ7Syh0avPYkC_nCP7VHhJAZ_2N2TpdticL0CXzDz518Q3bOpK6ez-HXvStdu6huN-a9vzZm5tuUHAAQ5roqUW3wdtkn4ovI6_qT7indPHMGvOLOTPhoW7xSiXYWMEjbV2mS_KuB6nvZ5y_POlv3A=w1146-h764-no",
"https://lh3.googleusercontent.com/hYMfd95j4KQpnvWlivAJm-UtJJYuUwULoYdFXsdlw3XN1sftwIpyC7nc2NaRNtoGkFHB86cVUeRUhIPRIOXvNAN9CSAjSG5-bHICmXq8AbMSrrchT4dWyZYBSrVXroNXEyVmEYZNC_KCaCiwGhkxITOZKwEILMpCXpIz-bLWCeBg7wAtqZiMYzsq3h8hhtbos8875mDMjw9R7KU0kfqy8zwTOgd-E5548u-mjEUh2ZaNnzlUSNNyYlac0NdMQonVVcHaNp-3880Ti9r6erBYjRWSVx1JAwtPp-2oAoVJPel6pYmRlllDWPzzKAIEvZqV2gniCP1poBLGTFlNuJ7WfNWz9NwDAX4wshOFZIEc3SI0NuYzyC-ZiwBRS4mVuEDr_dDhvDTLKal6YqlY0anXOhXs0h-2dKjaNi8806MJnmqeg6bX_3C6HKSkqJeheCaWTq2UFSuq5zj2iO2U1QMV1Kl7jt6oBz2V-oiipk2jKmsuvvuRciNHikG0hsI9mE1pG3j93ZNxLN1MLgRrfDwqSmM0q48So1suvF0bgj8m9d1KGhP9uFPuC1Nl5jL6TAiOI9bBAIp5Mbu-blRhXLJ2wWEQHCReyHBTI7bfy5EAvTbDMiANYrv2pG6lF1a4sIOFqLsgHPQJ-1U_1Zs2OKaq9gAxKJBVnO_zocnfdL0wUWv8U50VOGgW9hTxKZN-jHak7kPMJPgjmCKYMO-8g-qLFiFkDiviA-qDDbrzyGESZupQun8fmw=w1070-h764-no",
"https://lh3.googleusercontent.com/2GNERXAkBPa79ycqAC6JGpoUmB50J0OoVKKp0AT5D3ZU-yeSYA8nGnS3DYwz94KD7aU34ZdG6Zq7SIR0GbCFK93iMgRYfasBbJGreMPTmXQxSU6W0Tzn1U2gg_GPKdDhm3PL_5td3u201gKwKACQTS5GKGwVYwQpTM0pOhY-Fn3-zSvHI9IjEM4JGjgUMn_DfADtbuf8fzRBZffohWjWvkpcRGthxBcTmW1uSZgw6sjwE64KNyde65i9KuwMeLf02ymLtrjHg1SqeR6aIyQyDPDKdg2jHyxQaRZCnPdtvLIJ9qoIU7TUToqK-TSbzPXWFhBuWVRhTRTQC81nSlQNu1KhgY4nx750FUV5bdqvOv9HtOdjTIbOypM9AwOTTv3xRDhOmRkfA-Iuf5u_OJylHrc6THmwgcVfN3wX8LTK9xEbtsVVNWc_8oF-IZ8dxcSorwkzBXsrh3T8r5THXpuMLshYZOOdva5cn9G-J9Xv8T7UVskmu5eG0VqqhMwrj3fXQaiZ8ZmeemFn26p0J45SPRG_oekdy5fR-GkKFqtZF83Ur2jlCicaNTAEfi5Xq_lhxSbuNe9qYFZH4a-yQ77AhpzIxswvrUx7l9JFjz_EWesPot3QIhoTX9Us33nw4bPp4ZZ0i87Lp_HEka-1QmLQH3P1IZ5R2BK61fWlSMVWv8bX2qqWdAWQCEXhOwGwCUt3W-pCwFzwrndyZ80R2Pj1p3-1JC979x0j_CqV2Vi0VxZakMbZKQ=w1070-h764-no",
"https://lh3.googleusercontent.com/7RSUgRYBq7b1NdUn3qG6NGnpx-sQH0szQoxoysUGympUat1vQpudI_SuN3RQX14MmcJuCgJTd4EI-WYER7YG3ywOZ0iXr2Fm9Zs16IwOYjXjkGfO_Kj0po-81Zm8ch1LfF_WbabULh9ZDN-R4yn9tb05RHJJh19okWHNGlX30m_2_oJ_Go0NkUTHtPEf2BNoJSl297mgm2G3vcUk-X7o32iNiB8yNwC7FNwYvqszwH9l6Qx4PEP7qZ0MbIUWk-bDG40-hgh4CYmZDn4IVyNcMlLEn_haLf8RI3Z76XPleIyl7NQrbYktplj03ApVXxZifxMlZb_Qvgr6vjCp0B3gfIdI8N_OfRRnBYgt0pzSV-eVyDBrb7RKIdq54t8gmwMKQESJlhaEa2slZIdaZ69hqkn60fXPgcY2Aws3k2x2oYjm4-LHIRHo1Q5Ao_Vhe-KG8qFNj7X2DWwcoKRhLEQ3ihO6jfK6AoPGEQvEdDJoflMjA4ThUVBToaR6Etcg-VNWNwm7GtbcJAGEyQZB-sxeYDrstjlxdlY_WhXwme2JVFMYrkjMuejJ44uL3APGi49vV6XsknXn0l5aBccezGgc8T3oCXv4IiwZp55aNsR91gqbrwbPbJN9LQmo_n90ZO2rf6VwtqgPIj5rb5byAaHrNwaMuERGp-coSjT3IzqD6PutOqyJYFD2msm-8RN3oQwc9gKzkm1ygMS2Z7etwxAYhX7mr_95RlnER7yta8WebhMM9DMBYw=w1155-h764-no",
"https://lh3.googleusercontent.com/42dhZLCrBa5awrUcI3SuIauN_NDJeXKpHc3i31XCaCMLupp6vSSR9bj6iuIWZEj9HnMgbJDsbQAz_cbHC2Ky0doxLY3Qk1Ec3eTL6TetG53dYLYpMAaBFIG490KdQPSmbw2jHSlZf08dTbNs7sFOSso6jYMzx9Amaim559FTRz9KRsFnzfVTlIKRvCK5dmhSPywoWuswP2NHS7hQb_GvQk5pQUhKHpjLAgP_0VhbOPwm0YscbLH3MDPMeABvufwu4xP88IxAErrfvt7lNMCFw4sFB9j6mHsSeB8ORL-7WClhd8L6Dlb9nQs3Hj5ySb7pSolVZmrglAu3knzqgPLT98vcDaQDqxkUTN3DaXhl1batoHeh__FsrcsNkm85h_-o1ihNfBnCnQOcDQTXhSRFXAGvyidL0uwLapXTBPrFNg95lWPGa1WiBwIgDeIRWpwJrnTQynmRSeFYqOhXvb6vom7AluxcG-l8CsGPlRNOX6mgxsV25q8H76qvOzJh2qnA1-GnZQzv-osCkPf3egFulSIJlR2dLZewB1TS2FN3jrFbYAMdxzWgGACeD4DJqmN-fW3O5tcVCgqW5_nsrPC6enfOE0X7m-cYaQ-tnQrJrG20tYaaBkcQgUvkkqHjlQB1B7fJpxUMrl0K_FFWfGsCa5UztSUIKSu46ziwP3sRbXI9-Bs26QBhX0d-SUPgwvkzcYPvv33SaB0eKfNOXeRYJQ3CNs5DGZtrAK8zKbXjF4JbK_wNpA=w1147-h764-no",
"https://lh3.googleusercontent.com/ifSCtdZ-qX_tE0eCr08Elzp8gUmJjg6MBWsnGCW6pjzEoePwNQw7VNDn56kHKDvbysvdMebPqeh3TcHocFQmzT-egfxMjMuEOrNutRqpiaCmMK7dzSHXV7FF0iCrMPeHmoP8W6-8LAwvCiBTi_mjxrAAp_aQQ-mFCHT9h0hjUItMnCGwG6Oe33pWDHYJ1iUj4tqbvhTnH_NB0VKdXn5anXznvEYC4BMktUrmIRdn_gUkAvnHb-gAztSBHRhgM7W9hAON80WELNq8oND6mJzrP0CdZgTwICihD8TNWiXwMA6IgpOBffKPbJxXypNIDkfgtileExy9vbnsDgJHBzmLJPliAe-0is-NKfFVwIf2wAqCPxFuGfYZYdqnevFznvcMTpDIqZJzb9hvHfWLxnO37EEf1OoVZivjs6KyO11FMvw4WZgN2hfyn_jyNl-gyGi0JeHmuHK5FEhBK5Cg-qZe_0qy6VNA1CEdnxN8ANfOMWgvIZBQ6-Dq96A1Bau6CaCO5jRAhcZf0PW32P5m3fjowCY1sDXVIMOZ3gqTe-n_rK9jUy8X2ak-GEk-I1rOtEgV2i4DIExRS96Hp6n0zt6sC5X7uxy40GhMPYZhmyRlC1mk7fgwQ5McAUm8NfA-kDdbi5UpF_O7vJTtBp_FA7OdW8gd6DgXPD1LrNb0THb3Am0WyEkCxqsbGONEj2AqKJ4zFiLz_LQDZGoHxpfuvu21kTVG2u6-YS5pI-e4XqsrLLaeBEP5cQ=w1147-h764-no",
"https://lh3.googleusercontent.com/c2TVMd4UKuV1E3o4MYhf0VxVpqYcOi3_2JdY2z9X4rUE3tnxZ1AI9cbt3jJzhXzF0MWp1WzPpln03e3sRg6B3FeenDQ7X-IRKtjnS7isDYJlZAFb3OwWHpt9YVzU6KjYxdwdAJdV-ID-_tcz2xT6GvwkFGpzLvLXefLs1VRDz8JN21nemf-WvkCg_vNKXxoepo76ddVLxsZHO7K-XwXcPVpCVTtjcmYOXvoh8crqSvkJXahgZjhjTUw_1ae9snE1EoO3X0iFZ8gP-SKWb_Z25dClk1GzTN0OVRFAbysOzTO0MUNxlonfBOfuozgvQ4_6ZtpsVMBqmbqI57N7WOF_AmKUUaPuidHkeC8mZo6KkQEW7xDf2BmAKDpL0i4tGaaCn0UwhVKYCm35IF7aHhrhveU0kXylaQBPJPnaO99gHdQPqPUuCjN5S9o3geMxEgNQetEeO7F8mftxY9Tt8utQzIHV4KI5Joj-pU37p2UW1mY5An43wEhHUAIgs6VnGtU4EJFuT2QEhqZpurGoW32CSiRQ1Fy89iOWTrjAqOUQjdBrgw6T8NaSphWGIOpLaH9KsubmMtqrrSXkjcx_NKHk_RGoLykKNLLJXIQXUGGEVLQoO4O5nfx15CtqVtOqIiqUwoU_nB6QN_hjrnSXQQpeGISaMLo1hMxAqXG7xSGfJpSBwQddlxxuT3GHVBZ719Bfl575QuASUSTdoRBRiQScM-gGNcOfoc-Li3hHaaN4Hw2d5Oj30g=w1147-h764-no",
"https://lh3.googleusercontent.com/PnP4JuwBJzdC9v8coGEzxa0lruIdGpyNwEUxYQpMPEsy7QRzwzZXodxZzfEjm6bojZ0vEh_anVx7Udj6BUsJKGVrrQrMiiz0tdAF8N1IB_PSiFLmzmsIArMII8MFTH0etnMDh0jWi_LZyoxHNTaJgfK7wfRjRCIdBlnXlzP-jU3o-jMy-d0i0wXXL8Dt3yMj9zl7DgH9CmWSqdQRvqu-O8zQviKrhMLukXZY2VkHpgRKh4-oGulb6mm8hxMKh-8Wu-3XPdBMMWhslwMPEZ_x4h8vgDA8qeRl_tneiagJhhBvrZooye_DaI_pbi65aIzECoWQlWdrhLsDFN_VM6D7XU4YMsDYqfEI6PUIxf1sggybyF122DuLdTORzkYcOGRjFliWQ00_vqdKo_MLhYTgsgL9fc6gmgK_3rqhAQKolY-HN0fuWlO5dvFo8ttHoBBrT_TmgrfMQhKJRbS8Hfc8NuDCnOkEPTgnw0Ms6OaGH0fCdCXKJaDyfaMbQVYqq5OZ1SL4hHJ67Fv5Z3XMU78ZeX62R67YZ4Lw6qTnr1H8SRx7eF5lzI8Fx2yMtUA2Zz9div2PiCwdkIWDbgZvEOKiF5KGpi4XJkOGZwvHeAtw7nZ783Em3AtXP5u5ZBTkUGguumo9IY8Yd_qW_eNLbNxsoxYGqX6UHvhcWAQlxE8A3GttFCeUxU2BjdPbbE0NxIAl-x_aPWvufs9S94LinTe-NX7cnVYPzTe_kMuQhIRJbhKGZOprng=w1019-h764-no",
"https://lh3.googleusercontent.com/FvElOBreBYvD0ZcNb308MmStB6DUIx8_v-ymm342YBVFsZuYiswFvY5NEvVFyoK9x9jMnDOruKFN7xDQ-LO8sdsNT2OJU-OChKlnmEpIEH4fAjhZpAXp3MzPaL7dW4emeoQpGxrWf9Kayy-IoKrwPjLLI_GsiLKLE3tT9Wdc1Zw7DjwRjt08oeBt6lfxmnREtmYnWs1wSuvh1Rn6N5ZDbjUlql9rZb5BF38TbQxWAxh7LugCP3m7mvan0hsMMly4QpxQko8pZZAcQDJpwAJw7_r0wmPH4skdLNyickT9IUYQAQZpdTlN2lHqqfTtGCe__Kz4l9VxKBqGtWTlVk6EwKEIMiuQjdBIhm-5Va-l_emY415t5FjgmqAgNDQx1jnrfA_Qz4LQLZL_1CLluj55PKROq5WDlLh2CyQS6pQc0vCBvMmd4v2t47dpnaFEPxl-WKZJCe21mPhtPnZjNI_rQZC1jC0Yh6CQrrxy2fmcCKn4TjfhIiQAAvuiwD4TyfDpQckLzLMo2QoVl8IMpsMXemgHdwrGODdxt0IYGjQbQ0DRLjTe13gD_2D1U4j-sqtfMw-bA4clp5OxfMgbB3hQ0bFXVqI385x2Qko9uKjwYXtrPI-Q-sM_NzPaRZM4A9zbdaOFKaNAE-3x9zEtTJsiAS3jjusyQ6fuUF90Uxq343nA3wGyrz8N_MfSPATTUGw7IlSumgYNP4yLZ9-AVN6curoc5--TZSRcbkUA4_sd2bZUgs95uw=w1146-h764-no",
"https://lh3.googleusercontent.com/Opdvsi3M4G05xhzVYexU7GeVP1W_Qz5z1D6BoKkZMp6IcJdQ04nqrMIZpsS9522K37_45kBJXPOPBLjxl6d5z5V06iNBBpUxI06Kc-0_P0-L4qf0dFYXq2u6WCClBnN273eTSeX0ae4QnMoXjKI61_KALDGOev8LG1_gSayeQzXL-nYXxmZEQ_Wtgv6GRaiAD44d3PP0cCUxUbfscTBYJiyB7m2HXCUNDOfqWa22CTTWLurVAFdexBPwbxBPbVp_pmBLthXZel7bcD_iidzpC9T2Fs6wGeR3ITXxQip6imubWOPizvfvnKmOLnkVwcfOzRu8HjK_QjdSJaODlNFiS4Zt-9W0YWj5mFj3LPW_oO1G7rkmv7ZuGgBHCjASZW9UnVyEj4HscEvqWRyNlV5HtbC0oBOKTpXPb7nYd7oXcOkVb2QFoR9UvRNetmLby_R4uv4bfwh255ALlGJJiwrCt0feVBo108_FxeJH1CqsF1bxa872hj4-JFJ6g1AM-8eaGFxKccPqL4JoKgiudYFSAxdvvlWmkgG63pWvXzyudy1ZXu4C-f6PWMj9BtMrZ_buNZbdu7mFQCy9te44LUSxUg1Me3Oq9PzS0AyXPNDlZA_owabuhyLTlCP_MneNbXeMAnRUUe01qgvJfLkoJ5vN4LMWe5RhKvUxAj-L4yy68OinWqtu7UEOCb2DmSRRnIvQzHKWqT7GVyLzR4mqu_URHY3mogKFWx2Y2lhmMqvktCHeNytkpQ=w1147-h764-no",
"https://lh3.googleusercontent.com/bEFIN7cqhS8ml-mRJ6jdVFVQvhCVsuRIe8nvyOwe7WSsxSyBy0B6HhFeyc6jr6jSkCMdv9Qi3iNwUNKSpuGyEunVXgWtozzQie0PzYDSd-71-QjdiiMMULqrUymXGiLo8CUyqhXoOvAhmu06jd5kl_h0dOlGcGDu4PHjY-KNU6x9Qy2iw_3Ks09Nnup4LnBKEtRUpco68MKVHrFk5su836d1dbuu76hvHZaYSosb6788RFDNav5CBR0pomaNe2l8y4-vKzMbPpStb96v-TlEdJYAHjc2QCdH4wDJEd1R6mJY5cYY7wXrAhrn2XyGXCozWG8qsDgrhd7XBFQp6PeyhXMWJmuTDYKV5QGLLLf9UfK4mbE96l7diU5oDkWh_9Ux45-Tf_mM8sENrl4EKWPEBoJs4r9lV3-4RRmXVfzvoAhe5fUNi4bCXxqOmJl6OnrbaIU-77jPqLb9w7PopbxQguqYGKtsefmxMdFIt5NFt70W8i_Foh54apGpIAJMAxhmB7wGOqlIvP08F6un-mzxd8v0S8wBA4mFmQTiyWVdj3DZSthYde1jIZfdU7WWw8223LfnD7lPO5qFsjANHkin349vaTkW4-UJzJ6kWQh9_oDuPH89KDsMz7ozQk22RMDTZq4-RIcHBF82lFrBjW3e9D6X62YW0FaKxmPxkUfMqcyRqE6DgDh5HfIg_J8U0wTzI8UtxRS2wjjmMqJc4fUUpcx5vdCpgkM8fVnFrV4aeJ0IVc_4XQ=w1166-h764-no",
"https://lh3.googleusercontent.com/Pkkcv3lZi9xWfwBSXoliiu_f5xMylLfgMn4nXELa5KL6hhygDWuKCBDfl86xeV56H3myzfaOI4m9t50QSDtyWeHp44E5lHOxw7zmQ5gGjkoalT6p6rbSRFL2_UQ5I3q2yuVnmpsOao5sKgXP6PPu3ALaE6XdwiKlv11E5kczlUaYxufsM7GVnxr6aeLDnTMEPkz6Ej8udaQZLL1OYHxx8aWA7p33Eo_tSbDh1L9V0ikJVy-damaRQAoq1IE8p6VbBMgXHGbru7-IXDLabjlC2RJS1y1j1a2P58eBh6GWBj9-cCWfxt3kLUjgPLaarEhqmngO22hW-b6vMcpsJTb8rMrS-YyK6--D9bGM1JDZMltoUtPsPZxfGso4eChZua0gIpBGxWT85evYWqmKgwqzETyjxkHUnMUhp0tv82Fx8kQxbx9l8_W1ZMlayZdCzo2QYJ9q5HDVlKn1Wui2QoGBbWjz_10Jj7KOAf8ho3e77n7An7UVa59PJ5CeDjs38S3eKSLcpRR8rgYOGulTeSlsoaA695q8udfHWMsoTb7Wez83Bztc8-SE84JsOx7CbLZqQKySGbhVdX5p64FzHUS1z6P_6kxV5CwEduTBvrILK_zv98j4u9WGBkSr9xKtqqM_8IuPR4bwIYLfFXSYcwDzr3enTHbp5rnPU2IFTIQ-uD00Tsm9sxR1WKAZhow69e4t6VEcuJbPCm47Pd_W93-ndaTN2hj6pmXe_gGBngsejGYa6mQ0qw=w1070-h764-no",
"https://lh3.googleusercontent.com/95eap_o-2BAGcUTxvsCHiML9M-3FCOECeo04-WhgEgPqYBi4jYj2rHtPoTJGIrQ1ziV-YKtZ2VVQnhOuMEv-W9EnUUQmGHiienqrEM85M_cU3E6s-awSozWQfkDQPUWYe5MKP2mQ-RgV_WtVwoAZyBwDEJVWu6YbkTrnDBQMmzDm97d1x7BTb9Uc27UfZmFyCXQfaloU9JRYuWgMRvpAMcRypexMRzHdPIInepFnyRGU_GTocARjbS0w75jZgss_XSmIcCivG9cvnm_agh9ARVuJJjoBKThHvNHmQFwSFFyPEYMNaUn5Nfti1u5ClCMezx7-f1dh2i1v4bUMHZNk_YUj8qSlZ_N_A2e0hqIUlrGCnNpQ7srmP8eEFi-hBJsJGRG6khvNHrLBh3tJ6tl_a4GOCWfkwW_dnhYk1yzG6hjvlIoGx1GogXr8GXHUClMbPal0GpRXMdIcgWX80qZZZ0ut_JX4sj5i99WZZoSVmUU00F1IkcWB-8MR6il74Q2x3OICh56uJczQp2_LJSDvMuChD4yL5OReBW603VBdiIF2qkKjFW5_DwciRAuaoJIhM-hH2Z1HBrUJFg26vaWtvAob5H1cD-CldEIpg8NjpnA9DoJ8Zscu5_rGy2EExlwutl7Xnq_GbLXr11ai6fQpzjx34uDFwL6PnzAV-QiNv6cNLBvc56SoM86JQAx8DOeoOP4v-WVtqvfCGIATZURzCBLbpHFRmmD1x0eosROvnnEE-V16ug=w461-h307-no",
"https://lh3.googleusercontent.com/STlcWxwgIzg1ofkOy-GauddmXJl_Jnh_dEijAHMginvEuudoAgH8WjdrBYjmEPnhjDbUvozLyM4brK2zyXkyTqeGPxYe-1010pauurE1cQ8moGAh9z8EY-xjGitjR4FyQJ2cxNSgXCRaEhV5VMFZWeIg3JBo2r58z7xe4jzGXQhrZcTFhdvensPvdt_g93QMIFIW4tZGvcEomq0A6JVAFWUGKUKxlYToC4OFiMXNP9GKjudGTwDDUOvN9rMWO8k789QpyicxnpZr5NZjjAjWtLJE7XmtjEEm7UyGSh-5ID8MAeMHf0L1b21PrkKt9GNGEeI-oauSkjrTmpCyjqH3hej42v7cNgY9piVJKHXlYCWD6G-_6eUehG5THx3OsAcMfMAKqFmgDCQI0QvmKsuLXdPi53xfFGQTeQyfroZjhP-cOG-LsLRaAMEDd8xVQDEnskt2Pzvk_pxg0UcxN9kstTpkE-9cNCEqR_it0b2BJwMveXH5zvVq0QuF-Lb385vWVuJw84KPtFp2z90UDXJ3iEgtftbw0A4vfiSLhdGi73bZTOylidFWsxsVJevQEPI06Uxvw7TOqVtANT1cyYwla_JeRyPPU9J-UNrxluC5vFwW4hPG76aljhQcBVJnx9IHKdOPu2B_16qqWEFxogUORe3rJPc0Wn3-WDWtefmXPgjon9ZPmggPpmeYq4M4pjot9yDlqPWH2_ZkkiDU76og-t7il3rc33AWOkEZ1GdlmiwsYnfnTw=w1147-h764-no"
]


'''
                {% if photo_urls is defined %}
                    {% set count = 1 %}
           	        {% for photo in photo_urls %}
           	            {% if count < photo_urls|length|divide(3) %}
                            <div class="column">
                                <img src="{{ photo }}" style="width:100%">
                            </div>
                            {% set count = 1 %}
                        {% else %}
                            <img src="{{ photo }}" style="width:100%">
                            {% set count = count + 1 %}
                        {% endif %}
                    {% endfor %}
                {% else %}
                    <p>Something went wrong!</p>
                {% endif %}
'''
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thoughts.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class entries(db.Model):
	id = db.Column('entry_id', db.Integer, primary_key = True)
	name = db.Column(db.String(50))
	thought = db.Column(db.String(200))
	time = db.Column(db.String(100))

	def __init__(self, name, thought, time):
		self.name = name
		self.thought = thought
		self.time = time

'''


@app.route('/', endpoint='index')
def index():
	return render_template('index.html')

@app.route('/projects', endpoint='projects')
def projects():
	return render_template('projects.html')

@app.route('/books', endpoint='books')
def contact():
	return render_template('books.html')

@app.route('/WiiGA', endpoint='WiiGA')
def WiiGA():
	return render_template('WiiGA_Tour.html')

@app.route('/photos', endpoint='photos')
def photos():
    return render_template('photos.html', photo_urls = photo_urls)

@app.route('/projects/movie_barcode_generator', endpoint='movie barcode')
def AES_encryption():
	return render_template('movie_barcode_generator.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/projects/dalton_method', endpoint='dalton method', methods = ['GET', 'POST'])
def project462():
    if request.method == 'GET':
	    return render_template('dalton_method.html')
    else:
        # check if the post request has the file part
        file = request.files['file']
        if 'file' not in request.files or file == '':
            flash('No file inputted')
            return render_template('dalton_method.html')
        # if user does not select file, browser also
        # submit a empty part without filename
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test2.jpg'))
            dalton_method.dalton_run('/home/jpucilos/flask_website/static/test2.jpg')
            return render_template('dalton_method2.html')
        return render_template('dalton_method.html')


@app.route('/projects/rayleigh_fading', endpoint='rayleigh fading', methods = ['GET', 'POST'])
def project441():
    if request.method == 'GET':
	    return render_template('rayleigh_fading.html')
    else:
        # check if the post request has the file part
        try:
            f0 = int(request.form['f0'])
            v = int(request.form['v'])
            n = int(request.form['n'])
            fs = int(request.form['fs'])
            signal_fading_sim.rayleigh_fade(f0,v,n,fs)
        except ValueError as verr:
            print >> sys.stderr, str(verr)
        except Exception as ex:
            print >> sys.stderr, str(ex)

        return render_template('rayleigh_fading.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


'''
@app.route('/your-thoughts')
def index():
	if 'name' not in session:
		return redirect(url_for('login'))
	else:
		return render_template('show_yours.html', entries = reversed(entries.query.filter_by(name = session['name']).all()))
'''

'''
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		if 'name' in request.values:
			session['name'] = request.form['name']
		else:
			session['name'] = 'Anonymous'
		return redirect(url_for('show_all'))
'''


'''
@app.route('/new', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		if not request.form['thought']:
			flash('Please enter all the fields', 'error')
		else:
			entry = entries(session['name'], request.form['thought'], datetime.now().strftime('%Y-%m-%d at %H:%M'))

			db.session.add(entry)
			db.session.commit()
			flash('Record was successfully added')
			return redirect(url_for('show_all'))
	return render_template('new.html')
'''
if __name__ == '__main__':
    app.run(debug = False)

