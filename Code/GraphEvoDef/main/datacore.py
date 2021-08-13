# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021 - present Vijay Walunj
"""

class SoftwareMetric:

    def __init__(self, project, class_name, wmc, dit, noc, cbo, rfc, lcom, ca, ce, npm, lcom3, loc, dam, moa, mfa, cam, ic, cbm, amc, avg_cc, max_cc, defect_cnt):
        try:
            self.PROJECT_NAME = project
            self.CLASS_NAME = class_name
            try:
                if wmc.isdigit(): self.WMC = int(wmc)
            except ValueError:
                self.WMC = None
            try:
                if dit.isdigit(): self.DIT = int(dit)
            except ValueError:
                self.DIT = None
            try:
                if noc.isdigit(): self.NOC = int(noc)
            except ValueError:
                self.NOC = None
            try:
                if cbo.isdigit(): self.CBO = int(cbo)
            except ValueError:
                self.CBO = None
            try:
                if rfc.isdigit(): self.RFC = int(rfc)
            except ValueError:
                self.RFC = None
            try:
                if lcom.isdigit(): self.LCOM = int(lcom)
            except ValueError:
                self.LCOM = None
            try:
                if ca.isdigit(): self.Ca = int(ca)
            except ValueError:
                self.Ca = None
            try:
                if ce.isdigit(): self.Ce = int(ce)
            except ValueError:
                self.Ce = None
            try:
                if npm.isdigit(): self.NPM = int(npm)
            except ValueError:
                self.NPM = None
            try:
                if lcom3.replace('.', '', 1).isdigit(): self.LCOM3 = float(lcom3)
            except ValueError:
                self.LCOM3 = None
            try:
                if loc.isdigit(): self.LOC = int(loc)
            except ValueError:
                self.LOC = None
            try:
                if dam.replace('.', '', 1).isdigit():self.DAM = float(dam)
            except ValueError:
                self.DAM = None
            try:
                if moa.isdigit(): self.MOA = int(moa)
            except ValueError:
                self.MOA = None
            try:
                if mfa.replace('.', '', 1).isdigit(): self.MFA = float(mfa)
            except ValueError:
                self.MFA = None
            try:
                if cam.replace('.', '', 1).isdigit(): self.CAM = float(cam)
            except ValueError:
                self.CAM = None
            try:
                if ic.isdigit(): self.IC = int(ic)
            except ValueError:
                self.IC = None
            try:
                if cbm.isdigit(): self.CBM = int(cbm)
            except ValueError:
                self.CBM = None
            try:
                if amc.replace('.', '', 1).isdigit():self.AMC = float(amc)
            except ValueError:
                self.AMC = None
            try:
                self.AVG_CC = int(avg_cc)
            except ValueError:
                self.AVG_CC = None
            try:
                self.MAX_CC = int(max_cc)
            except ValueError:
                self.MAX_CC = None
            self.PORTRAIT = None
            self.NEWONE = None
            self.DEFECT_CNT = defect_cnt
        finally:
            print("Error occured")

    def add_portrait_metrics(self, newone, portrait):
        try:
            self.PORTRAIT = portrait
            self.NEWONE = newone
        finally:
            print("Error ocurred")