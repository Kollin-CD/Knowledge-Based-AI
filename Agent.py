# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageFilter, ImageMath
import numpy as np
import math
# TODO: Implement Structural Similarity?

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.problemSpace = []
        self.answerSpace = []
        self.transformationSpace = []
        self.problemMap = {}
        self.answerMap = {}
        self.problemArrays = {}
        self.answerArrays = {}
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        return self.image_loop(problem)

    '''
    Main function that takes in a problem from the API

    Note: Experimental code is commented out

    Returns: a value -1, 1:6
    '''
    def image_loop(self, problem):
        # Identify the type of problem
        # print("\nProblem Name: " + problem.name)
        # print("Problem Type: " + problem.problemType)
        # print("Problem Set: " + problem.problemSetName)

        if problem.problemType == "3x3":
            problemType = 3
            diff1 = 0
        else:
            problemType = 2

        # Loop through the problem dict
        for figure_key, figure_values in problem.figures.items():
            # print("\n" + figure_key + ": " + figure_values.visualFilename)
            # Separate into RPM problems and answers
            if figure_key.isdigit():
                # Store image as is with PIL
                self.answerSpace.append(figure_values)
                self.answerArrays[figure_key] = figure_values

                # Convert to numpy array
                im = Image.open(figure_values.visualFilename)
                im_data = self.convert_to_black_and_white_array(im)
                self.answerMap[figure_key] = im_data
            else:
                # size = 128, 128
                self.problemSpace.append(figure_values)
                self.problemArrays[figure_key] = figure_values
                # Convert to numpy array
                im = Image.open(figure_values.visualFilename)
                # Filter first
                im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
                # Change to a black and white np array
                im_data = self.convert_to_black_and_white_array(im)

                self.problemMap[figure_key] = im_data
                # print(im_data.shape) verify that it is the same as above

        ######################################################################
        '''
        Use PIL Images
        '''
        if problemType != 3:
            diff1, diff2, diff3, result = self.solve_2x2_RPM(problem)

            # horizontal & vertical (IPR)
            # intersection ratio pseudocode:
            # ((left & right).blackPixels / left.blackPixels) -
            # ((uut & answer).blackPixels / uut.blackPixels)

        elif problemType == 3:
            # First Line
            imageA = Image.open(problem.figures["A"].visualFilename)
            imageB = Image.open(problem.figures["B"].visualFilename)
            imageC = Image.open(problem.figures["C"].visualFilename)
            # Second Line
            imageD = Image.open(problem.figures["D"].visualFilename)
            imageE = Image.open(problem.figures["E"].visualFilename)
            imageF = Image.open(problem.figures["F"].visualFilename)
            # Third Line
            imageG = Image.open(problem.figures["G"].visualFilename)
            imageH = Image.open(problem.figures["H"].visualFilename)

            # Horizontal Analogy
            # print("\nHorizontal Analogy: ")
            horiz_value_1 = self.analogy_1(imageA, imageB)
            horiz_value_2 = self.analogy_1(imageB, imageC)
            horiz_value_3 = self.analogy_1(imageD, imageE)
            horiz_value_4 = self.analogy_1(imageE, imageF)
            horiz_value_5 = self.analogy_1(imageG, imageH)

            horiz_value_6 = self.analogy_1(imageA, imageC)
            horiz_value_7 = self.analogy_1(imageD, imageF)
            avg_horiz_test_value = (horiz_value_6 + horiz_value_7)/2

            diff_horiz_1 = abs(horiz_value_1 - horiz_value_2)
            diff_horiz_2 = abs(horiz_value_3 - horiz_value_4)
            diff_horiz_3 = abs(horiz_value_6 - horiz_value_7)

            avg_diff_horiz_value = (diff_horiz_1 + diff_horiz_2)/2

            # Vertical Analogy
            vert_value_1 = self.analogy_1(imageA, imageD)
            vert_value_2 = self.analogy_1(imageD, imageG)
            vert_value_3 = self.analogy_1(imageB, imageE)
            vert_value_4 = self.analogy_1(imageE, imageH)
            vert_value_5 = self.analogy_1(imageC, imageF)

            vert_value_6 = self.analogy_1(imageA, imageG)
            vert_value_7 = self.analogy_1(imageB, imageH)
            avg_vert_test_value = (vert_value_6 + vert_value_7) / 2

            diff_vert_1 = abs(vert_value_1 - vert_value_2)
            diff_vert_2 = abs(vert_value_3 - vert_value_4)
            diff_vert_3 = abs(vert_value_6 - vert_value_7)
            avg_diff_vert_value = (diff_vert_1 + diff_vert_2)/2

            # Diagonal Analogy
            # print("\nDiagonal Analogy: ")
            diag_value_1 = self.analogy_1(imageB, imageF)
            diag_value_2 = self.analogy_1(imageF, imageG)
            diag_value_3 = self.analogy_1(imageC, imageD)
            diag_value_4 = self.analogy_1(imageD, imageH)
            diag_value_5 = self.analogy_1(imageA, imageE)

            diag_value_6 = self.analogy_1(imageB, imageG)
            diag_value_7 = self.analogy_1(imageC, imageH)
            avg_diag_test_value = (diag_value_6 + diag_value_7) / 2

            diff_diag_1 = abs(diag_value_1 - diag_value_2)
            diff_diag_2 = abs(diag_value_3 - diag_value_4)
            diff_diag_3 = abs(diag_value_6 - diag_value_7)

            avg_diff_diag_value = (diff_diag_1 + diff_diag_2)/2

            # DPS
            mod_imageA = imageA.convert(mode='L', dither=Image.NONE)
            mod_imageB = imageB.convert(mode='L', dither=Image.NONE)
            mod_imageC = imageC.convert(mode='L', dither=Image.NONE)
            mod_imageD = imageA.convert(mode='L', dither=Image.NONE)
            mod_imageE = imageB.convert(mode='L', dither=Image.NONE)
            mod_imageF = imageC.convert(mode='L', dither=Image.NONE)
            mod_imageG = imageA.convert(mode='L', dither=Image.NONE)
            mod_imageH = imageB.convert(mode='L', dither=Image.NONE)

            imageA_and_B = ImageChops.logical_or(imageA.convert(mode="1"), imageB.convert(mode="1"))
            horiz_logic_1 = self.analogy_1(imageA_and_B,imageC)
            imageD_and_E = ImageChops.logical_or(imageD.convert(mode="1"), imageE.convert(mode="1"))
            horiz_logic_2 = self.analogy_1(imageD_and_E,imageF)

            w, h = 8, 1
            answer_list_4 = [[999 for x in range(w)] for y in range(h)]

            if horiz_logic_1 < 50 and horiz_logic_2 < 50:
                flag_1 = 1
                # print(problem.name)
                imageG_and_H = ImageChops.logical_or(imageG.convert(mode="1"), imageH.convert(mode="1"))
                for answer_key, answer_values in self.answerArrays.items():
                    imageAnswer = Image.open(answer_values.visualFilename)
                    test_horiz_logic = self.analogy_1(imageG_and_H, imageAnswer)

                    if test_horiz_logic < 50:
                        answer_list_4[0][int(answer_key) - 1] = abs(test_horiz_logic)

                # print(answer_list_4, "\n")
            else:
                flag_1 = 0

            imageA_and_D = ImageChops.logical_and(imageA.convert(mode="1"), imageD.convert(mode="1"))
            vert_logic_1 = self.analogy_1(imageA_and_D, imageG)
            imageB_and_E = ImageChops.logical_and(imageB.convert(mode="1"), imageE.convert(mode="1"))
            vert_logic_2 = self.analogy_1(imageB_and_E, imageH)
            w, h = 8, 1
            answer_list_5 = [[999 for x in range(w)] for y in range(h)]

            if vert_logic_1 < 50 and vert_logic_2 < 50:
                flag_2 = 1
                # print(problem.name)
                imageC_and_F = ImageChops.logical_and(imageC.convert(mode="1"), imageF.convert(mode="1"))
                for answer_key, answer_values in self.answerArrays.items():
                    imageAnswer = Image.open(answer_values.visualFilename)
                    test_vert_logic = self.analogy_1(imageC_and_F, imageAnswer)

                    imageCF_and_Ans = ImageChops.logical_and(imageAnswer.convert(mode="1"),imageC_and_F)
                    imageCF_or_Ans = ImageChops.logical_or(imageAnswer.convert(mode="1"), imageC_and_F)

                    # print(self.dps_func(imageCF_and_Ans.getdata()))
                    dpsCF_Ans = (self.dps_func(imageCF_and_Ans.getdata())/self.dps_func(imageCF_or_Ans.getdata()))

                    if test_vert_logic < 50:
                        answer_list_5[0][int(answer_key) - 1] = abs(test_vert_logic)

                # print(answer_list_5, "\n")
            else:
                flag_2 = 0

        ######################################################################
        '''
        Use only the ImageChops method from PIL
        IPR_A = number_of_dark_pixel_at_same_coordinates_in_A_and_B / number_of_dark_pixels(A) 
        IPR_B = number_of_dark_pixel_at_same_coordinates_in_A_and_B / number_of_dark_pixels(B) 
        IPR = IPR_A - IPR_B
        
        DPS = number of dark pixels / total pixels
        '''
        ######################################################################

        if problemType == 3:

            dpsA = self.dps_func(mod_imageA.getdata())
            dpsB = self.dps_func(mod_imageB.getdata())
            dpsC = self.dps_func(mod_imageC.getdata())
            dpsD = self.dps_func(mod_imageD.getdata())
            dpsE = self.dps_func(mod_imageE.getdata())
            dpsF = self.dps_func(mod_imageF.getdata())
            dpsG = self.dps_func(mod_imageG.getdata())
            dpsH = self.dps_func(mod_imageH.getdata())

            # Horizontal
            imageA_and_B = ImageChops.logical_or(imageA.convert(mode="1"), imageB.convert(mode="1"))
            mod_imageA_and_B = imageA_and_B.convert(mode='L', dither=Image.NONE)
            dpsA_and_B = self.dps_func(mod_imageA_and_B.getdata())
            imageA_and_C = ImageChops.logical_or(imageA.convert(mode="1"), imageC.convert(mode="1"))
            mod_imageA_and_C = imageA_and_C.convert(mode='L', dither=Image.NONE)
            dpsA_and_C = self.dps_func(mod_imageA_and_C.getdata())
            imageB_and_C = ImageChops.logical_or(imageB.convert(mode="1"), imageC.convert(mode="1"))
            mod_imageB_and_C = imageB_and_C.convert(mode='L', dither=Image.NONE)
            dpsB_and_C = self.dps_func(mod_imageB_and_C.getdata())
            imageD_and_E = ImageChops.logical_or(imageD.convert(mode="1"), imageE.convert(mode="1"))
            mod_imageD_and_E = imageD_and_E.convert(mode='L', dither=Image.NONE)
            dpsD_and_E = self.dps_func(mod_imageD_and_E.getdata())
            imageD_and_F = ImageChops.logical_or(imageD.convert(mode="1"), imageF.convert(mode="1"))
            mod_imageD_and_F = imageD_and_F.convert(mode='L', dither=Image.NONE)
            dpsD_and_F = self.dps_func(mod_imageD_and_F.getdata())
            imageE_and_F = ImageChops.logical_or(imageE.convert(mode="1"), imageF.convert(mode="1"))
            mod_imageE_and_F = imageE_and_F.convert(mode='L', dither=Image.NONE)
            dpsE_and_F = self.dps_func(mod_imageE_and_F.getdata())
            imageG_and_H = ImageChops.logical_or(imageG.convert(mode="1"), imageH.convert(mode="1"))
            mod_imageG_and_H = imageG_and_H.convert(mode='L', dither=Image.NONE)
            dpsG_and_H = self.dps_func(mod_imageG_and_H.getdata())

            iprA = dpsA_and_B / dpsA
            iprB = dpsA_and_B / dpsB
            iprAB = abs(iprA - iprB)
            iprA = dpsA_and_C / dpsA
            iprC = dpsA_and_C / dpsC
            iprAC = abs(iprA - iprC)
            iprB = dpsB_and_C / dpsB
            iprC = dpsB_and_C / dpsC
            iprBC = abs(iprB - iprC)
            iprD = dpsD_and_E / dpsD
            iprE = dpsD_and_E / dpsE
            iprDE = abs(iprD - iprE)
            iprD = dpsD_and_F / dpsD
            iprF = dpsD_and_F / dpsF
            iprDF = abs(iprD - iprF)
            iprE = dpsE_and_F / dpsE
            iprF = dpsE_and_F / dpsF
            iprEF = abs(iprE - iprF)
            iprG = dpsG_and_H / dpsG
            iprH = dpsG_and_H / dpsH
            iprGH = abs(iprG - iprH)

            horiz_weighted_ipr_1 = iprAB * 0.333 + iprAC * 0.333 + iprBC * 0.333
            horiz_weighted_ipr_2 = iprDE * 0.333 + iprDF * 0.333 + iprEF * 0.333
            horiz_weighted_ipr_3 = horiz_weighted_ipr_1 * 0.333 + horiz_weighted_ipr_2 * 0.333
            # print("Weighted IPR 1: ", horiz_weighted_ipr_1)
            # print("Weighted IPR 2: ", horiz_weighted_ipr_2)
            # print("Weighted IPR 3: ", horiz_weighted_ipr_3)

            w, h = 8, 3
            answer_list_3 = [[999 for x in range(w)] for y in range(h)]
            zero_list_3 = [[999 for x in range(w)] for y in range(h)]

            # Horizontal
            for answer_key, answer_values in self.answerArrays.items():
                imageAnswer = Image.open(answer_values.visualFilename)
                mod_imageAns = imageAnswer.convert(mode='L', dither=Image.NONE)
                dpsAns = self.dps_func(mod_imageAns.getdata())

                imageG_and_Ans = ImageChops.logical_or(imageG.convert(mode="1"), imageAnswer.convert(mode="1"))
                # imageG_and_Ans.show()
                mod_imageG_and_Ans = imageG_and_Ans.convert(mode='L', dither=Image.NONE)
                dpsG_and_Ans = self.dps_func(mod_imageG_and_Ans.getdata())

                imageH_and_Ans = ImageChops.logical_or(imageH.convert(mode="1"), imageAnswer.convert(mode="1"))
                mod_imageH_and_Ans = imageH_and_Ans.convert(mode='L', dither=Image.NONE)
                dpsH_and_Ans = self.dps_func(mod_imageH_and_Ans.getdata())

                iprAns_1 = dpsG_and_Ans / dpsAns
                iprAns_2 = dpsH_and_Ans / dpsAns
                iprAns_3 = iprGH

                weighted_Ans = iprAns_3 * 0.333 + iprAns_1 * 0.333 + iprAns_2 * 0.333

                horiz_ans_value_1 = abs(iprAns_1 - horiz_weighted_ipr_1)
                horiz_ans_value_2 = abs(iprAns_2 - horiz_weighted_ipr_1)
                horiz_ans_value_3 = abs(iprAns_1 - horiz_weighted_ipr_2)
                horiz_ans_value_4 = abs(iprAns_2 - horiz_weighted_ipr_2)
                horiz_ans_value_5 = abs(iprAns_1 - horiz_weighted_ipr_3)
                horiz_ans_value_6 = abs(iprAns_2 - horiz_weighted_ipr_3)
                horiz_ans_value_7 = abs(weighted_Ans - horiz_weighted_ipr_3)

                # print("Image: ", answer_key)
                # print("Answer Value 1: ", horiz_ans_value_1)
                # print("Answer Value 2: ", horiz_ans_value_2)
                # print("Answer Value 3: ", horiz_ans_value_3)
                # print("Answer Value 4: ", horiz_ans_value_4)
                # print("Answer Value 5: ", horiz_ans_value_5)
                # print("Answer Value 6: ", horiz_ans_value_6)
                # print("Answer Value 7: ", horiz_ans_value_7)

                answer_list_3[0][int(answer_key) - 1] = abs(horiz_ans_value_7)

            for x in range(0, 3):
                zero_list_3[0][np.argmin(answer_list_3[0])] = min(answer_list_3[0])
                answer_list_3[0][np.argmin(answer_list_3[0])] = 999

            # Vertical
            imageA_and_D = ImageChops.logical_or(imageA.convert(mode="1"), imageD.convert(mode="1"))
            mod_imageA_and_D = imageA_and_D.convert(mode='L', dither=Image.NONE)
            dpsA_and_D = self.dps_func(mod_imageA_and_D.getdata())
            imageA_and_G = ImageChops.logical_or(imageA.convert(mode="1"), imageG.convert(mode="1"))
            mod_imageA_and_G = imageA_and_G.convert(mode='L', dither=Image.NONE)
            dpsA_and_G = self.dps_func(mod_imageA_and_G.getdata())
            imageD_and_G = ImageChops.logical_or(imageD.convert(mode="1"), imageG.convert(mode="1"))
            mod_imageD_and_G = imageD_and_G.convert(mode='L', dither=Image.NONE)
            dpsD_and_G = self.dps_func(mod_imageD_and_G.getdata())
            imageB_and_E = ImageChops.logical_or(imageB.convert(mode="1"), imageE.convert(mode="1"))
            mod_imageB_and_E = imageB_and_E.convert(mode='L', dither=Image.NONE)
            dpsB_and_E = self.dps_func(mod_imageB_and_E.getdata())
            imageB_and_H = ImageChops.logical_or(imageB.convert(mode="1"), imageH.convert(mode="1"))
            mod_imageB_and_H = imageB_and_H.convert(mode='L', dither=Image.NONE)
            dpsB_and_H = self.dps_func(mod_imageB_and_H.getdata())
            imageE_and_H = ImageChops.logical_or(imageE.convert(mode="1"), imageH.convert(mode="1"))
            mod_imageE_and_H = imageE_and_H.convert(mode='L', dither=Image.NONE)
            dpsE_and_H = self.dps_func(mod_imageE_and_H.getdata())
            imageC_and_F = ImageChops.logical_or(imageC.convert(mode="1"), imageF.convert(mode="1"))
            mod_imageC_and_F = imageC_and_F.convert(mode='L', dither=Image.NONE)
            dpsC_and_F = self.dps_func(mod_imageC_and_F.getdata())

            iprA = dpsA_and_D / dpsA
            iprD = dpsA_and_D / dpsD
            iprAD = abs(iprA - iprD)
            iprA = dpsA_and_G / dpsA
            iprG = dpsA_and_G / dpsG
            iprAG = abs(iprA - iprG)
            iprD = dpsD_and_G / dpsD
            iprG = dpsD_and_G / dpsG
            iprDG = abs(iprD - iprG)
            iprB = dpsB_and_E / dpsB
            iprE = dpsD_and_E / dpsE
            iprBE = abs(iprB - iprE)
            iprB = dpsB_and_H / dpsB
            iprH = dpsB_and_H / dpsH
            iprBH = abs(iprB - iprH)
            iprE = dpsE_and_H / dpsE
            iprH = dpsE_and_H / dpsH
            iprEH = abs(iprE - iprH)
            iprC = dpsC_and_F / dpsC
            iprF = dpsC_and_F / dpsF
            iprCF = abs(iprC - iprF)

            vert_weighted_ipr_1 = iprAD * 0.333 + iprAG * 0.333 + iprDG * 0.333
            vert_weighted_ipr_2 = iprBE * 0.333 + iprBH * 0.333 + iprEH * 0.333
            vert_weighted_ipr_3 = vert_weighted_ipr_1 * 0.333 + vert_weighted_ipr_2 * 0.333

            # Vertical
            for answer_key, answer_values in self.answerArrays.items():
                imageAnswer = Image.open(answer_values.visualFilename)
                mod_imageAns = imageAnswer.convert(mode='L', dither=Image.NONE)
                dpsAns = self.dps_func(mod_imageAns.getdata())

                imageC_and_Ans = ImageChops.logical_or(imageC.convert(mode="1"), imageAnswer.convert(mode="1"))
                mod_imageC_and_Ans = imageC_and_Ans.convert(mode='L', dither=Image.NONE)
                dpsC_and_Ans = self.dps_func(mod_imageC_and_Ans.getdata())

                imageF_and_Ans = ImageChops.logical_or(imageF.convert(mode="1"), imageAnswer.convert(mode="1"))
                mod_imageF_and_Ans = imageF_and_Ans.convert(mode='L', dither=Image.NONE)
                dpsF_and_Ans = self.dps_func(mod_imageF_and_Ans.getdata())

                iprAns_1 = dpsC_and_Ans / dpsAns
                iprAns_2 = dpsF_and_Ans / dpsAns
                iprAns_3 = iprCF

                weighted_Ans = iprAns_3 * 0.333 + iprAns_1 * 0.333 + iprAns_2 * 0.333

                vert_ans_value_1 = abs(iprAns_1 - vert_weighted_ipr_1)
                vert_ans_value_2 = abs(iprAns_2 - vert_weighted_ipr_1)
                vert_ans_value_3 = abs(iprAns_1 - vert_weighted_ipr_2)
                vert_ans_value_4 = abs(iprAns_2 - vert_weighted_ipr_2)
                vert_ans_value_5 = abs(iprAns_1 - vert_weighted_ipr_3)
                vert_ans_value_6 = abs(iprAns_2 - vert_weighted_ipr_3)
                vert_ans_value_7 = abs(weighted_Ans - vert_weighted_ipr_3)

                # print("Image: ", answer_key)
                # print("Answer Value 1: ", vert_ans_value_1)
                # print("Answer Value 2: ", vert_ans_value_2)
                # print("Answer Value 3: ", vert_ans_value_3)
                # print("Answer Value 4: ", vert_ans_value_4)
                # print("Answer Value 5: ", vert_ans_value_5)
                # print("Answer Value 6: ", vert_ans_value_6)
                # print("Answer Value 7: ", vert_ans_value_7)

                answer_list_3[1][int(answer_key) - 1] = abs(vert_ans_value_7)

            for x in range(0, 3):
                zero_list_3[1][np.argmin(answer_list_3[1])] = min(answer_list_3[1])
                answer_list_3[1][np.argmin(answer_list_3[1])] = 999

            # Diagonal
            imageA_and_E = ImageChops.logical_or(imageA.convert(mode="1"), imageE.convert(mode="1"))
            mod_imageA_and_E = imageA_and_E.convert(mode='L',dither=Image.NONE)
            dpsA_and_E = self.dps_func(mod_imageA_and_E.getdata())
            imageB_and_F = ImageChops.logical_or(imageB.convert(mode="1"), imageF.convert(mode="1"))
            mod_imageB_and_F = imageB_and_F.convert(mode='L', dither=Image.NONE)
            dpsB_and_F = self.dps_func(mod_imageB_and_F.getdata())
            imageB_and_G = ImageChops.logical_or(imageB.convert(mode="1"), imageG.convert(mode="1"))
            mod_imageB_and_G = imageB_and_G.convert(mode='L', dither=Image.NONE)
            dpsB_and_G = self.dps_func(mod_imageB_and_G.getdata())
            imageF_and_G = ImageChops.logical_or(imageF.convert(mode="1"), imageG.convert(mode="1"))
            mod_imageF_and_G = imageF_and_G.convert(mode='L', dither=Image.NONE)
            dpsF_and_G = self.dps_func(mod_imageF_and_G.getdata())
            imageC_and_D = ImageChops.logical_or(imageC.convert(mode="1"), imageD.convert(mode="1"))
            mod_imageC_and_D = imageC_and_D.convert(mode='L', dither=Image.NONE)
            dpsC_and_D = self.dps_func(mod_imageC_and_D.getdata())
            imageC_and_H = ImageChops.logical_or(imageC.convert(mode="1"), imageH.convert(mode="1"))
            mod_imageC_and_H = imageC_and_H.convert(mode='L', dither=Image.NONE)
            dpsC_and_H = self.dps_func(mod_imageC_and_H.getdata())
            imageD_and_H = ImageChops.logical_or(imageD.convert(mode="1"), imageH.convert(mode="1"))
            mod_imageD_and_H = imageD_and_H.convert(mode='L', dither=Image.NONE)
            dpsD_and_H = self.dps_func(mod_imageD_and_H.getdata())

            iprA = dpsA_and_E / dpsA
            iprE = dpsA_and_E / dpsE
            iprAE = abs(iprA - iprE)
            iprB = dpsB_and_F / dpsB
            iprF = dpsB_and_F / dpsF
            iprBF = abs(iprB - iprF)
            iprB = dpsB_and_G / dpsB
            iprG = dpsB_and_G / dpsG
            iprBG = abs(iprB - iprG)
            iprF = dpsF_and_G / dpsF
            iprG = dpsF_and_G / dpsG
            iprFG = abs(iprF - iprG)
            iprC = dpsC_and_D / dpsC
            iprD = dpsC_and_D / dpsD
            iprCD = abs(iprC - iprD)
            iprC = dpsC_and_H / dpsC
            iprH = dpsC_and_H / dpsH
            iprCH = abs(iprC - iprH)
            iprD = dpsD_and_H / dpsD
            iprH = dpsD_and_H / dpsH
            iprDH = abs(iprD - iprH)

            diag_weighted_ipr_1 = iprBF * 0.333 + iprBG * 0.333 + iprFG * 0.333
            diag_weighted_ipr_2 = iprCD * 0.333 + iprCH * 0.333 + iprDH * 0.333
            diag_weighted_ipr_3 = diag_weighted_ipr_1 * 0.333 + diag_weighted_ipr_2 * 0.333

            # Diagonal
            for answer_key, answer_values in self.answerArrays.items():
                imageAnswer = Image.open(answer_values.visualFilename)
                mod_imageAns = imageAnswer.convert(mode='L', dither=Image.NONE)
                dpsAns = self.dps_func(mod_imageAns.getdata())

                imageA_and_Ans = ImageChops.logical_or(imageA.convert(mode="1"), imageAnswer.convert(mode="1"))
                mod_imageA_and_Ans = imageA_and_Ans.convert(mode='L', dither=Image.NONE)
                dpsA_and_Ans = self.dps_func(mod_imageA_and_Ans.getdata())

                imageE_and_Ans = ImageChops.logical_or(imageE.convert(mode="1"), imageAnswer.convert(mode="1"))
                mod_imageE_and_Ans = imageE_and_Ans.convert(mode='L', dither=Image.NONE)
                dpsE_and_Ans = self.dps_func(mod_imageE_and_Ans.getdata())

                iprAns_1 = dpsA_and_Ans / dpsAns
                iprAns_2 = dpsE_and_Ans / dpsAns
                iprAns_3 = iprAE

                weighted_Ans = iprAns_3 * 0.333 + iprAns_1 * 0.333 + iprAns_2 * 0.333

                diag_ans_value_1 = abs(iprAns_1 - diag_weighted_ipr_1)
                diag_ans_value_2 = abs(iprAns_2 - diag_weighted_ipr_1)
                diag_ans_value_3 = abs(iprAns_1 - diag_weighted_ipr_2)
                diag_ans_value_4 = abs(iprAns_2 - diag_weighted_ipr_2)
                diag_ans_value_5 = abs(iprAns_1 - diag_weighted_ipr_3)
                diag_ans_value_6 = abs(iprAns_2 - diag_weighted_ipr_3)
                diag_ans_value_7 = abs(weighted_Ans - diag_weighted_ipr_3)

                # print("Image: ", answer_key)
                # print("Answer Value 1: ", diag_ans_value_1)
                # print("Answer Value 2: ", diag_ans_value_2)
                # print("Answer Value 3: ", diag_ans_value_3)
                # print("Answer Value 4: ", diag_ans_value_4)
                # print("Answer Value 5: ", diag_ans_value_5)
                # print("Answer Value 6: ", diag_ans_value_6)
                # print("Answer Value 7: ", diag_ans_value_7)

                answer_list_3[2][int(answer_key) - 1] = abs(diag_ans_value_7)

            for x in range(0, 3):
                zero_list_3[2][np.argmin(answer_list_3[2])] = min(answer_list_3[2])
                answer_list_3[2][np.argmin(answer_list_3[2])] = 999

            # DPS
            horiz_dps_1 = (dpsA - dpsB)/33857
            horiz_dps_2 = (dpsA - dpsC)/33857
            horiz_dps_3 = (dpsB - dpsC)/33857
            horiz_dps_4 = (dpsD - dpsE)/33857
            horiz_dps_5 = (dpsD - dpsF)/33857
            horiz_dps_6 = (dpsE - dpsF)/33857
            horiz_dps_7 = (dpsG - dpsH)/33857

            horiz_first_row = (horiz_dps_1 + horiz_dps_2 + horiz_dps_3)/3
            horiz_second_row = (horiz_dps_4 + horiz_dps_5 + horiz_dps_6)/3
            horiz_weighted = horiz_first_row*.333 + horiz_second_row*0.333 + horiz_dps_7*.333

            vert_dps_1 = (dpsA - dpsD)/33857
            vert_dps_2 = (dpsA - dpsG)/33857
            vert_dps_3 = (dpsD - dpsG)/33857
            vert_dps_4 = (dpsB - dpsE)/33857
            vert_dps_5 = (dpsB - dpsH)/33857
            vert_dps_6 = (dpsE - dpsH)/33857
            vert_dps_7 = (dpsC - dpsF)/33857

            vert_first_row = (vert_dps_1 + vert_dps_2 + vert_dps_3) / 3
            vert_second_row = (vert_dps_4 + vert_dps_5 + vert_dps_6) / 3
            vert_weighted = vert_first_row * .333 + vert_second_row * 0.333 + vert_dps_7 * .333

            diag_dps_1 = (dpsB - dpsF) / 33857
            diag_dps_2 = (dpsB - dpsG) / 33857
            diag_dps_3 = (dpsF - dpsG) / 33857
            diag_dps_4 = (dpsC - dpsD) / 33857
            diag_dps_5 = (dpsC - dpsH) / 33857
            diag_dps_6 = (dpsD - dpsH) / 33857
            diag_dps_7 = (dpsA - dpsE) / 33857

            diag_first_row = (diag_dps_1 + diag_dps_2 + diag_dps_3) / 3
            diag_second_row = (diag_dps_4 + diag_dps_5 + diag_dps_6) / 3
            diag_weighted = diag_first_row * .333 + diag_second_row * 0.333 + diag_dps_7 * .333

            w, h = 8, 3
            answer_list = [[999 for x in range(w)] for y in range(h)]
            zero_list = [[999 for x in range(w)] for y in range(h)]

            w, h = 8, 3
            answer_list_2 = [[999 for x in range(w)] for y in range(h)]
            zero_list_2 = [[999 for x in range(w)] for y in range(h)]

            # Test the horizontal aspect
            # A:B:C :: D:E:F :: G:H:?  figure out ? in this block of code
            answer_image = Image.open(problem.figures["H"].visualFilename)
            test_image = Image.open(problem.figures["G"].visualFilename)
            test_image_2 = Image.open(problem.figures["D"].visualFilename)

            for answer_key, answer_values in self.answerArrays.items():

                imageAnswer = Image.open(answer_values.visualFilename)

                answer_value = self.analogy_1(answer_image, imageAnswer)
                test_value = self.analogy_1(test_image, imageAnswer)
                test_value_2 = self.analogy_1(test_image_2, imageAnswer)

                temp_value = abs(answer_value - avg_diff_horiz_value - horiz_value_5)
                temp_value_2 = abs(avg_horiz_test_value - test_value)

                if avg_diff_horiz_value < 0.5 and abs(horiz_value_5 - test_value) < 0.5:
                    temp_value = abs(horiz_value_5 - test_value)

                if diff_horiz_3 < 0.5 and abs(horiz_value_5 - test_value - diff_horiz_3) < 2:
                    temp_value = abs(horiz_value_5 - test_value - diff_horiz_3)

                if test_value == 0 and avg_diff_horiz_value > 0.02:
                    temp_value = 999

                if test_value_2 < 5 and avg_diff_horiz_value > 0.02:
                    temp_value = 999

                answer_list[0][int(answer_key) - 1] = temp_value

                # DPS Method
                imageAnswer_2 = imageAnswer.convert(mode='L', dither=Image.NONE)
                dpsAns = self.dps_func(imageAnswer_2.getdata())

                horiz_answer_value_1 = (dpsG - dpsAns)/33857
                horiz_answer_value_2 = (dpsH - dpsAns)/33857

                vert_answer_value_1 = (dpsC - dpsAns)/33857
                vert_answer_value_2 = (dpsF - dpsAns)/33857

                diag_answer_value_1 = (dpsA - dpsAns)/33857
                diag_answer_value_2 = (dpsE - dpsAns)/33857

                horiz_temp_value_2 = (horiz_answer_value_1 + horiz_answer_value_2 - 2*horiz_weighted) / 2
                vert_temp_value_2 = (vert_answer_value_1 + vert_answer_value_2 - 2*vert_weighted) / 2
                diag_temp_value_2 = (diag_answer_value_1 + diag_answer_value_2 - 2*diag_weighted) / 2

                answer_list_2[0][int(answer_key) - 1] = abs(horiz_temp_value_2)
                answer_list_2[1][int(answer_key) - 1] = abs(vert_temp_value_2)
                answer_list_2[2][int(answer_key) - 1] = abs(diag_temp_value_2)

                # print("horiz_answer_1: ", horiz_answer_value_1)
                # print("horiz_answer_2: ", horiz_answer_value_2)
                # print("horiz_temp_value_2: ", horiz_temp_value_2)

            if np.mean(answer_list[0]) > 8:
                for x in range(0, 3):
                    # Write to zero_list (should contain the 3 smallest values)
                    if min(answer_list[0]) > np.mean(answer_list[0]):
                        zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 5
                    elif min(answer_list[0]) > 10:
                        zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 4
                    elif min(answer_list[0]) > 5:
                        zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 3
                    elif min(answer_list[0]) > 1:
                        zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 2
                    else:
                        zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0])

                    # Write over the smallest values in answer_list
                    answer_list[0][np.argmin(answer_list[0])] = 999
            else:
                for x in range(0, 7):
                    zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0])
                    # Write over the smallest values in answer_list
                    answer_list[0][np.argmin(answer_list[0])] = 999

            for x in range(0, 3):
                if min(answer_list_2[0]) > 25:
                    zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 5
                    zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 5
                    zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 5
                elif min(answer_list_2[0]) > 10:
                    zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 4
                    zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 4
                    zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 4
                elif min(answer_list_2[0]) > 5:
                    zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 3
                    zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 3
                    zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 3
                elif min(answer_list_2[0]) > 2:
                    zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 2
                    zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 2
                    zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 2
                else:
                    zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0])
                    zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1])
                    zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2])

                answer_list_2[0][np.argmin(answer_list_2[0])] = 999
                answer_list_2[1][np.argmin(answer_list_2[1])] = 999
                answer_list_2[2][np.argmin(answer_list_2[2])] = 999

            # Test the vertical aspect
            # A:D:G :: B:E:H :: C:F:? figure out ? in this block of code
            answer_image = Image.open(problem.figures["F"].visualFilename)
            test_image = Image.open(problem.figures["C"].visualFilename)
            for answer_key, answer_values in self.answerArrays.items():
                imageAnswer = Image.open(answer_values.visualFilename)

                answer_value = self.analogy_1(answer_image, imageAnswer)
                test_value = self.analogy_1(test_image, imageAnswer)

                temp_value = abs(answer_value - avg_diff_vert_value - vert_value_5)

                if avg_diff_vert_value < 0.72 and abs(vert_value_5 - test_value - diff_vert_3) < 0.5:
                    temp_value = abs(vert_value_5 - test_value - diff_vert_3)

                if test_value == 0 and avg_diff_vert_value > 0.02:
                    temp_value = 999

                answer_list[1][int(answer_key) - 1] = temp_value

            # Get the smallest three differences and assign weights for larger
            # differences
            if np.mean(answer_list[1]) > 36:
                for x in range(0, 3):
                    # Write to zero_list (should contain the 3 smallest values
                    if min(answer_list[1]) > 25:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 5
                    elif min(answer_list[1]) > 10:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 4
                    elif min(answer_list[1]) > 5:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 3
                    elif min(answer_list[1]) > 1:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 2
                    else:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1])

                    # Write over the smallest values in answer_list
                    answer_list[1][np.argmin(answer_list[1])] = 999
            elif np.mean(answer_list[1]) > 8:
                for x in range(0, 4):
                    # Write to zero_list (should contain the 3 smallest values
                    if min(answer_list[1]) > 32:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 5
                    elif min(answer_list[1]) > 16:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 4
                    elif min(answer_list[1]) > 8:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 3
                    elif min(answer_list[1]) > 4:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 2
                    else:
                        zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1])

                    # Write over the smallest values in answer_list
                    answer_list[1][np.argmin(answer_list[1])] = 999
            else:
                for x in range(0, 7):
                    zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1])

                    # Write over the smallest values in answer_list
                    answer_list[1][np.argmin(answer_list[1])] = 999

            # Test the diagonal aspect
            # B:F:G :: C:D:H :: A:E:? figure out the ? in this block of code
            answer_image = Image.open(problem.figures["E"].visualFilename)
            test_image = Image.open(problem.figures["A"].visualFilename)

            for answer_key, answer_values in self.answerArrays.items():
                imageAnswer = Image.open(answer_values.visualFilename)

                answer_value = self.analogy_1(answer_image, imageAnswer)
                test_value = self.analogy_1(test_image, imageAnswer)

                temp_value = abs(answer_value - avg_diff_diag_value - diag_value_5)

                if test_value == 0 and avg_diff_horiz_value > 0.02:
                    temp_value = 999

                answer_list[2][int(answer_key) - 1] = temp_value

            # Get the smallest three differences and assign weights for larger
            # differences
            diag_mean = np.mean(answer_list[2])
            for x in range(0, 4):
                # Write to zero_list (should contain the 3 smallest values
                if min(answer_list[2]) > diag_mean*1:
                    zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 5
                elif min(answer_list[2]) > diag_mean*0.8:
                    zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 4
                elif min(answer_list[2]) > diag_mean*0.6:
                    zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 3
                elif min(answer_list[2]) > diag_mean * 0.3:
                    zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 2
                else:
                    zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2])

                # Write over the smallest values in answer_list
                answer_list[2][np.argmin(answer_list[2])] = 999

        # Print out zero_list
        '''
        print("\n")
        for row in zero_list:
            for elem in row:
                print(round(elem,4), end=" ")
            print("\n")

        for row in zero_list_2:
            for elem in row:
                print(round(elem, 4), end=" ")
            print("\n")

        for row in zero_list_3:
            for elem in row:
                print(round(elem, 4), end=" ")
            print("\n")
        # print("\n************************************************************")
        '''
        '''    
        for row in answer_list:
            for elem in row:
                print(round(elem,4), end=" ")
            print("\n")
        '''

        if problemType == 3:
            answer_array = np.array(zero_list)
            answer_array_2 = np.array(zero_list_2)
            answer_array_3 = np.array(zero_list_3)
            answer_array_4 = np.array(answer_list_4)
            answer_array_5 = np.array(answer_list_5)
            total_average_array = answer_array.sum(axis=0) / 3
            total_average_array_2 = answer_array_2.sum(axis=0) / 3
            total_average_array_3 = answer_array_3.sum(axis=0) /3
            product_array = answer_array.prod(axis=0)
            product_array_2 = answer_array_2.prod(axis=0)
            product_array_3 = answer_array_3.prod(axis=0)

            result_array = [np.argmin(total_average_array) + 1, np.argmin(product_array) + 1,
                            np.argmin(total_average_array_2) + 1, np.argmin(product_array_2) + 1,
                            np.argmin(product_array_3) + 1, np.argmin(total_average_array_3) + 1]

            # print(result_array)

            result_array_2 = [np.argmin(answer_array_2, axis=1),
                              np.argmin(answer_array_3,axis=1)]

            # print(result_array_2)

            temp = np.array([], dtype=int)
            for elem2 in result_array_2:
                elem2 = elem2+1
                temp = np.append(temp, elem2)

            count = 0
            count2 = 0
            count3 = 0
            count4 = 0
            count5 = 0
            result = 0
            result2 = 0
            result3 = 0
            result4 = 0
            result5 = 0
            for elem in temp:
                if count == 0 and count2 == 0:
                    result = elem
                    count += 1
                else:
                    if elem == result:
                        count += 1
                    elif count2 == 0:
                        result2 = elem
                        count2 += 1
                    elif elem == result2:
                        count2 += 1
                    elif count3 == 0:
                        result3 = elem
                        count3 += 1
                    elif elem == result3:
                        count3 += 1
                    elif count4 == 0:
                        result4 = elem
                        count4 +=1
                    elif elem == result4:
                        count4 += 1
                    elif count5 == 0:
                        result5 = elem
                        count5 += 1
                    elif elem == result5:
                        count5 += 1

            count_array = np.array([count,count2,count3,count4,count5])
            count_array = np.argwhere(count_array==np.amax(count_array)).flatten()

            # print(temp)
            # print(count_array)
            idx = count_array[0]
            result = temp[idx]

            if (np.min(answer_array_4) != 999) or (np.min(answer_array_5) != 999):
                if (np.min(answer_array_4) < np.min(answer_array_5)):
                    result = np.argmin(answer_array_4) + 1
                else:
                    result = np.argmin(answer_array_5) + 1
            # print("Result: " + str(result))

            if (np.min(answer_array_5) != 999):
                diff1, diff2, diff3 = self.find_three_min(answer_array_5)
                if diff1 < 5 or diff2 < 5:
                    result = -1

        return result

    # noinspection PyMethodMayBeStatic
    def convert_to_black_and_white_array(self, image):
        im = image.convert("L")
        im_data = np.asarray(im, dtype="float32")

        return im_data

    # RMS Algorithm
    # Use just PIL
    # http://effbot.org/zone/pil-comparing-images.htm
    # https://medium.com/human-in-a-machine-world/mae-and-rmse-which-metric-is-better-e60ac3bde13d
    # https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
    # lines 427 and 428 are from pyimageseach.com
    # noinspection PyMethodMayBeStatic
    def compare_images_pil_rms(self, imageA, imageB):
        # Filter first
        imageA = imageA.filter(ImageFilter.GaussianBlur(radius=2))
        imageB = imageB.filter(ImageFilter.GaussianBlur(radius=2))

        # Return abs value of (imageA - imageB) pixel-by-pixel
        dif = ImageChops.difference(imageA, imageB)
        out = ImageMath.eval("a**2", a=dif)
        # List of pixel squared and their counts

        sq = []
        out = out.load()
        for i in range(0, imageA.size[0]):
            for j in range(0, imageB.size[1]):
                sq.append(out[i, j])

        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(imageA.size[0] * imageA.size[1]))

        return rms

    # RMS Algorithm
    # NOT CURRENTLY USED
    '''
    # Uses numpy arrays
    # https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
    # lines 441 and 442 are from the site
    # noinspection PyMethodMayBeStatic
    def compare_images_numpy_rms(self, imageA, imageB):
        # the 'Mean Squared Error' between the two images is the
        # sum of the squared difference between the two images;
        # NOTE: the two images must have the same dimension
        sum_of_squares = np.sum((imageA - imageB) ** 2)
        sum_of_squares = sum_of_squares/(imageA.shape[0] * imageA.shape[1])
        rms = math.sqrt(sum_of_squares)
        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return rms
    '''

    # Check sizes to be the same, I have to make a better function
    # noinspection PyMethodMayBeStatic
    def check_size(self, imageA, imageB):
        if imageA.width != imageB.width:
            width = 184
        else:
            width = imageA.width

        if imageA.height != imageB.height:
            height = 184
        else:
            height = imageB.height

        if imageA.width == imageB.width and imageA.height == imageB.height:
            # imageA = imageA.filter(ImageFilter.GaussianBlur(radius=1.5)) # Contour, Blur
            # imageB = imageB.filter(ImageFilter.GaussianBlur(radius=1.5)) # Smooth More (fill agnostic)
            resized_imageA = imageA
            resized_imageB = imageB
        else:
            resized_imageA = imageA.resize((width, height), Image.BILINEAR)
            resized_imageB = imageB.resize((width, height), Image.BILINEAR)

        return resized_imageA, resized_imageB

    # Comparison that returns a similarity value (RMSE)
    def analogy_1(self, imageA, imageB):
        # Check the size
        imageA, imageB = self.check_size(imageA, imageB)
        # Filter and
        # Run it through RMS Algorithm
        transformation_value = self.compare_images_pil_rms(imageA.convert("L"),
                                                           imageB.convert("L"))

        return transformation_value

    # NOT USED
    '''
    def analogy_2(self, imageA, imageB):
        # Resize or sample image
        imageA_width = imageA.shape[0]
        imageA_height = imageA.shape[1]
        imageB_width = imageB.shape[0]
        imageB_height = imageB.shape[1]

        # Run it through MSE Algorithm
        other_value = self.compare_images_numpy_rms(imageA, imageB)

        return other_value

    # Classify the transformation
    # 5 unchanged
    # 4 reflected
    # 3 rotated
    # 2 scaled
    # 1 deleted
    # 0 shape changed
    def classify(self, transformation_value, compared_image):
        if transformation_value == 0:
            # print("\nNo transformation")
            self.transformationSpace.append(5)
            return compared_image
        # print("Unknown")
        return compared_image
    '''

    # Get the differences among the smallest 4 values in an array
    # noinspection PyMethodMayBeStatic
    def find_three_min(self, array):
        length = len(array)
        array = sorted(array)
        diff = []

        for i in range(length-1):
            temp = array[i+1] - array[i]
            diff.append(temp)

        if not diff:
            diff1 = 999
            diff2 = 999
            diff3 = 999
        else:
            diff1 = diff[0]
            diff2 = diff[1]
            diff3 = diff[2]

        return diff1, diff2, diff3

    def solve_2x2_RPM(self, problem):
        imageA = Image.open(problem.figures["A"].visualFilename)
        imageB = Image.open(problem.figures["B"].visualFilename)
        imageC = Image.open(problem.figures["C"].visualFilename)

        mod_imageA = imageA.convert(mode='L', dither=Image.NONE)
        mod_imageB = imageB.convert(mode='L', dither=Image.NONE)
        mod_imageC = imageC.convert(mode='L', dither=Image.NONE)

        # horizontal & vertical (DPS)
        pixelsA = mod_imageA.getdata()
        pixelsB = mod_imageB.getdata()
        pixelsC = mod_imageC.getdata()

        black_thresh = 127

        nblack = 0
        for pixel in pixelsA:
            if pixel < black_thresh:
                nblack += 1
        n = len(pixelsA)
        dpsA = nblack / float(n)

        # print("Image A: %s" % (nblack / float(n)))

        nblack = 0
        for pixel in pixelsB:
            if pixel < black_thresh:
                nblack += 1
        n = len(pixelsB)
        dpsB = nblack / float(n)

        # print("Image B: %s" % (nblack / float(n)))

        nblack = 0
        for pixel in pixelsC:
            if pixel < black_thresh:
                nblack += 1
        n = len(pixelsC)
        dpsC = nblack / float(n)

        # print("Image C: %s" % (nblack / float(n)))

        #Horizontal Analogy
        horiz_value_1 = self.analogy_1(imageA, imageB)

        # Vertical Analogy
        vert_value_1 = self.analogy_1(imageA, imageC)

        # Diagonal Analogy
        diag_value_1 = self.analogy_1(imageB, imageC)

        horiz_dps_1 = (dpsA - dpsB)

        vert_dps_1 = (dpsA - dpsC)

        # diag_dps_1 = (dpsB - dpsC)

        w, h = 6, 3
        answer_list = [[999 for x in range(w)] for y in range(h)]
        zero_list = [[999 for x in range(w)] for y in range(h)]

        answer_list_2 = [[999 for x in range(w)] for y in range(h)]
        zero_list_2 = [[999 for x in range(w)] for y in range(h)]

        # Test the horizontal aspect
        # A:B :: C:? figure out ? in this block of code
        # Test the vertical aspect
        # A:C :: B:? figure out ? in this block of code
        # Test the diagonal aspect
        # B:C :: A:? figure out the ? in this block of code

        for answer_key, answer_values in self.answerArrays.items():
            # RMS Method
            imageAnswer = Image.open(answer_values.visualFilename)

            horiz_answer_value = self.analogy_1(imageC, imageAnswer)
            vert_answer_value = self.analogy_1(imageB, imageAnswer)
            diag_answer_value = self.analogy_1(imageA, imageAnswer)

            horiz_temp_value = abs(horiz_answer_value - horiz_value_1)
            vert_temp_value = abs(vert_answer_value - vert_value_1)
            diag_temp_value = abs(diag_answer_value - diag_value_1)

            # DPS Method
            imageAnswer_2 = imageAnswer.convert(mode='L', dither=Image.NONE)

            pixelsAnswer = imageAnswer_2.getdata()

            nblack = 0
            for pixel in pixelsAnswer:
                if pixel < black_thresh:
                    nblack += 1
            n = len(pixelsAnswer)

            # print("Image: ", int(answer_key), "has a dps of: ", (nblack/float(n)))

            horiz_answer_value_2 = (dpsC - (nblack / float(n)))
            vert_answer_value_2 = (dpsB - (nblack / float(n)))
            # diag_answer_value_2 = (dpsA - (nblack/ float(n)))

            horiz_temp_value_2 = (horiz_answer_value_2 - horiz_dps_1)
            vert_temp_value_2 = (vert_answer_value_2 - vert_dps_1)
            # diag_temp_value_2 = (diag_answer_value_2 - diag_dps_1)
            # Negative horiz, vert, diag dps means it is getting darker in that direction
            # print("Horizontal DPS Answer: ", int(answer_key), " : ", horiz_answer_value_2, " : ", horiz_dps_1)
            # print("Vertical DPS Answer: ", int(answer_key), " : ", vert_answer_value_2, " : ", vert_dps_1)
            # print("Diagonal DPS Answer: ", int(answer_key), " : ", diag_answer_value_2, " : ", diag_dps_1)

            answer_list[0][int(answer_key) - 1] = horiz_temp_value
            answer_list[1][int(answer_key) - 1] = vert_temp_value
            answer_list[2][int(answer_key) - 1] = diag_temp_value
            answer_list_2[0][int(answer_key) - 1] = abs(horiz_temp_value_2)
            answer_list_2[1][int(answer_key) - 1] = abs(vert_temp_value_2)
            # answer_list_2[2][int(answer_key) - 1] = abs(diag_temp_value_2)

        # Get the smallest three differences and assign weights for larger
        # differences
        for x in range(0, 3):
            # Write to zero_list (should contain the 3 smallest values
            if min(answer_list[0]) > 25:
                zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 5
            elif min(answer_list[0]) > 10:
                zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 4
            elif min(answer_list[0]) > 5:
                zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 3
            elif min(answer_list[0]) > 2:
                zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0]) * 2
            else:
                zero_list[0][np.argmin(answer_list[0])] = min(answer_list[0])

            if min(answer_list_2[0]) > 25:
                zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 5
            elif min(answer_list_2[0]) > 10:
                zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 4
            elif min(answer_list_2[0]) > 5:
                zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 3
            elif min(answer_list_2[0]) > 2:
                zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0]) * 2
            else:
                zero_list_2[0][np.argmin(answer_list_2[0])] = min(answer_list_2[0])

            if min(answer_list[1]) > 25:
                zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 5
            elif min(answer_list[1]) > 10:
                zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 4
            elif min(answer_list[1]) > 5:
                zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 3
            elif min(answer_list[1]) > 1:
                zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1]) * 2
            else:
                zero_list[1][np.argmin(answer_list[1])] = min(answer_list[1])

            if min(answer_list_2[1]) > 25:
                zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 5
            elif min(answer_list_2[1]) > 10:
                zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 4
            elif min(answer_list_2[1]) > 5:
                zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 3
            elif min(answer_list_2[1]) > 1:
                zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1]) * 2
            else:
                zero_list_2[1][np.argmin(answer_list_2[1])] = min(answer_list_2[1])

            if min(answer_list[2]) > 25:
                zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 5
            elif min(answer_list[2]) > 10:
                zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 4
            elif min(answer_list[2]) > 5:
                zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 3
            elif min(answer_list[2]) > 1:
                zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2]) * 2
            else:
                zero_list[2][np.argmin(answer_list[2])] = min(answer_list[2])

            if min(answer_list_2[2]) > 25:
                zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 5
            elif min(answer_list_2[2]) > 10:
                zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 4
            elif min(answer_list_2[2]) > 5:
                zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 3
            elif min(answer_list_2[2]) > 1:
                zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2]) * 2
            else:
                zero_list_2[2][np.argmin(answer_list_2[2])] = min(answer_list_2[2])

            # Write over the smallest values in answer_list
            answer_list[0][np.argmin(answer_list[0])] = 999
            answer_list[1][np.argmin(answer_list[1])] = 999
            answer_list[2][np.argmin(answer_list[2])] = 999
            answer_list_2[0][np.argmin(answer_list_2[0])] = 999
            answer_list_2[1][np.argmin(answer_list_2[1])] = 999
            answer_list_2[2][np.argmin(answer_list_2[2])] = 999

        answer_array = np.array(zero_list)
        answer_array_2 = np.array(zero_list_2)
        total_average_array = answer_array.sum(axis=0) / 3
        total_average_array_2 = answer_array_2.sum(axis=0) / 3
        product_array = answer_array.prod(axis=0)
        product_array_2 = answer_array_2.prod(axis=0)

        diff1, diff2, diff3 = self.find_three_min(total_average_array)

        # print("\n1st Diff: " + str(diff1))
        # print("2nd Diff: " + str(diff2))
        # print("3rd Diff: " + str(diff3) + "\n")

        # Print out zero_list
        '''
        print("\nZero List:\n")
        for row in zero_list:
            for elem in row:
                print(round(elem,4), end=" ")
            print("\n")
        print("\n************************************************************")
        print("\nZero List 2:\n")
        for row in zero_list_2:
            for elem in row:
                print(round(elem, 4), end=" ")
            print("\n")
        print("\n************************************************************")
        Print out answer_list
        print("\nAnswer List: ")
        for row in answer_list:
            for elem in row:
                print(round(elem,4), end=" ")
             print("\n")
        print("Average Array\n")
        print(np.around(total_average_array, decimals=2), sep=" ")
        print("************************************************************")
        print("Average Array 2\n")
        print(np.around(total_average_array_2, decimals=2), sep=" ")
        print("************************************************************")
        print("Product Array\n")
        print(np.around(product_array, decimals=2), sep=" ")
        print("************************************************************")
        print("Product Array 2\n")
        print(np.around(product_array_2, decimals=2), sep=" ")
        print("************************************************************")

        print("\nAverage Min: ")
        print(min(total_average_array))
        print("\nAverage Min 2: ")
        print(min(total_average_array_2))
        print("RMS Answer: ")
        print(np.argmin(total_average_array)+1)
        print("DPS Answer: ")
        print(np.argmin(total_average_array_2)+1)
        print("************************************************************")
        print("Main Min: ")
        print(min(product_array))
        print("Main Min 2: ")
        print(min(product_array_2))
        print("Main Answer: ")
        print(np.argmin(product_array) + 1)
        print("Main Answer 2: ")
        print(np.argmin(product_array_2) + 1)
        '''
        result_array = [np.argmin(total_average_array)+1, np.argmin(total_average_array_2)+1, np.argmin(product_array)+1, np.argmin(product_array_2) + 1]

        count = 0
        count2 = 0
        count3 = 0
        result = 0
        result2 = 0
        result3 = 0
        for elem in result_array:
            if count == 0 and count2 == 0:
                result = elem
                count += 1
            else:
                if elem == result:
                    count += 1
                elif count2 == 0:
                    result2 = elem
                    count2 += 1
                elif elem == result2:
                    count2 += 1
                elif count3 == 0:
                    result3 = elem
                    count3 += 1
                elif elem == result3:
                    count3 += 1

        # print("COUNT 1: ", count, "Count 2: ", count2)
        if count == count2:
            if min(product_array) / 100 > min(total_average_array):
                result = np.argmin(total_average_array) + 1
            else:
                result = np.argmin(product_array) + 1
        elif (count + count2) < 4:
            result = np.argmin(product_array) + 1
        elif count2 > count:
            result = result2


        # If one min is significantly larger than the other use the other
        # if min(product_array) / 1000 > min(total_average_array):
        #     result = np.argmin(total_average_array) + 1
        # else:
        #     result = np.argmin(product_array) + 1

        # print("RESULT: ", result)
        return diff1, diff2, diff3, result

    def dps_func(self, pixelsImage):
        black_thresh = 127
        dps = 0
        nblack = 0
        for pixel in pixelsImage:
            if pixel < black_thresh:
                nblack += 1
        n = len(pixelsImage)
        dps = nblack / float(n)

        # print("Lenth: ")
        # print(float(n))

        return nblack+1