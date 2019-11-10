# coding: utf-8
from sqlalchemy import Column, Float, Integer, String, text
from geoalchemy2.types import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import logging

Base = declarative_base()
metadata = Base.metadata


class Plant(Base):
    __tablename__ = 'plant'

    seqplt16 = Column(Integer, primary_key=True)
    pstatabb = Column(String)
    pname = Column(String)
    orispl = Column(Integer)
    oprname = Column(String)
    oprcode = Column(Integer)
    utlsrvnm = Column(String)
    utlsrvid = Column(Integer)
    baname = Column(String)
    bacode = Column(String)
    nerc = Column(String)
    subrgn = Column(String)
    srname = Column(String)
    isorto = Column(String)
    fipsst = Column(Integer)
    fipscnty = Column(Integer)
    cntyname = Column(String)
    lat = Column(Float(53))
    lon = Column(Float(53))
    numblr = Column(Integer)
    numgen = Column(Integer)
    plprmfl = Column(String)
    plfuelct = Column(String)
    coalflag = Column(String)
    capfac = Column(Float(53))
    namepcap = Column(Float(53))
    nbfactor = Column(Float(53))
    rmbmflag = Column(String)
    chpflag = Column(String)
    usethrmo = Column(Integer)
    pwrtoht = Column(Integer)
    elcalloc = Column(Float(53))
    psflag = Column(String)
    plhtian = Column(Integer)
    plhtioz = Column(Integer)
    plhtiant = Column(Integer)
    plhtiozt = Column(Integer)
    plngenan = Column(Integer)
    plngenoz = Column(Integer)
    plnoxan = Column(Integer)
    plnoxoz = Column(Integer)
    plso2an = Column(Integer)
    plco2an = Column(Integer)
    plch4an = Column(Integer)
    pln2oan = Column(Integer)
    plco2eqa = Column(Integer)
    plhgan = Column(Integer)
    plnoxrta = Column(Float(53))
    plnoxrto = Column(Float(53))
    plso2rta = Column(Float(53))
    plco2rta = Column(Integer)
    plch4rta = Column(Float(53))
    pln2orta = Column(Float(53))
    plc2erta = Column(Integer)
    plhgrta = Column(Integer)
    plnoxra = Column(Float(53))
    plnoxro = Column(Float(53))
    plso2ra = Column(Float(53))
    plco2ra = Column(Float(53))
    plhgra = Column(Integer)
    plnoxcrt = Column(Float(53))
    plnoxcro = Column(Float(53))
    plso2crt = Column(Float(53))
    plco2crt = Column(Float(53))
    plch4crt = Column(Float(53))
    pln2ocrt = Column(Integer)
    plhgcrt = Column(Integer)
    unnox = Column(Integer)
    unnoxoz = Column(Integer)
    unso2 = Column(Integer)
    unco2 = Column(Integer)
    unch4 = Column(Integer)
    unn2o = Column(Integer)
    unhg = Column(Integer)
    unhti = Column(Integer)
    unhtioz = Column(Integer)
    unhtit = Column(Integer)
    unhtiozt = Column(Integer)
    unnoxsrc = Column(String)
    unnozsrc = Column(String)
    unso2src = Column(String)
    unco2src = Column(String)
    unch4src = Column(String)
    unn2osrc = Column(String)
    unhgsrc = Column(String)
    unhtisrc = Column(String)
    unhozsrc = Column(String)
    plhtrt = Column(Integer)
    plgenacl = Column(Integer)
    plgenaol = Column(Integer)
    plgenags = Column(Integer)
    plgenanc = Column(Integer)
    plgenahy = Column(Integer)
    plgenabm = Column(Integer)
    plgenawi = Column(Integer)
    plgenaso = Column(Integer)
    plgenagt = Column(Integer)
    plgenaof = Column(Integer)
    plgenaop = Column(Integer)
    plgenatn = Column(Integer)
    plgenatr = Column(Integer)
    plgenath = Column(Integer)
    plgenacy = Column(Float(53))
    plgenacn = Column(Float(53))
    plclpr = Column(Float(53))
    plolpr = Column(Float(53))
    plgspr = Column(Float(53))
    plncpr = Column(Float(53))
    plhypr = Column(Float(53))
    plbmpr = Column(Float(53))
    plwipr = Column(Float(53))
    plsopr = Column(Float(53))
    plgtpr = Column(Float(53))
    plofpr = Column(Float(53))
    ploppr = Column(Float(53))
    pltnpr = Column(Float(53))
    pltrpr = Column(Float(53))
    plthpr = Column(Float(53))
    plcypr = Column(Float(53))
    plcnpr = Column(Float(53))
    geom = Column(Geometry('POINT', 4269))

    @property
    def annual_net_generation_state_percentage(self):
        """
        Returns the percentage of this plant's annual net
        generation contribution to the state's total.

        This query is expensive, and the result doesn't change
        very often. Implementing caching of some sort would
        improve performance.

        :return: a percentage.
        """
        from app import session
        query_result = session.query(func.sum(Plant.plngenan)
                             .filter(Plant.pstatabb == self.pstatabb)).all()
        percentage = None
        try:
            if self.plngenan:
                percentage = (self.plngenan / query_result[0][0]) * 100
        except Exception as e:
            logging.error('Error [{0}] when computing state contribution percentage for plant [{1}].'
                          .format(e, self))
        return percentage