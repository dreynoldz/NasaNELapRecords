from project.server import db
from flask import request
from project.server.models import User, Car, CarRacer, RaceClass, Racer, RacerSponsor, Track, TrackEvent, \
Event, Sponsor, BestLap, Setting, Page
from project.server.admin.forms import BestLapForm, CreateUserForm, UpdateUserForm, \
    passwordResetForm, NameSNForm, EventForm, CarForm,RacerForm,SponsorForm,SettingsForm,PagesForm

# Helper Functions
class DataServices():

    def get_model(model_name):
        return db.session.query(model_name)

    def get_modelOrder(data, model_name, order):
        if model_name == 'User':
            col = 'last_login'
        elif model_name == 'Event':
            col = 'start_date'
        else:
            col = 'id'
        model = eval(model_name)
        column = getattr(model, col)
        column_sorted = getattr(column, order)()
        return data.order_by(column_sorted)
    
    def get_filterBy(model_name, col, val, isFirst):
        filter = {col: val}
        if isFirst == True:
            return db.session.query(model_name).filter_by(**filter).first()
        else:
            return DataServices.get_model(model_name).filter_by(**filter).all()
    
    def get_modelChoices(model_name, col):
        choices = DataServices.get_model(model_name)
        choice_list = [(0, "---")]
        f = getattr(model_name, col)
        [choice_list.append((c.id, c.name)) for c in choices.order_by(f).all()]
        return choice_list

    def get_carChoices():
        cars = DataServices.get_model(Car)
        car_list = [(0, "---")]
        [car_list.append((c.id, c.number + ' ' + c.make + ' ' + c.model)) for c in cars.order_by(Car.number).all()]
        print("car_list")
        print(car_list)
        return car_list

    def remove_car_association(racer_id):
        racer = db.session.query(Racer).filter_by(id=racer_id)
        r = racer.first()
        carRacers = db.session.query(CarRacer).filter_by(racerId=racer_id).all()
        for carRacer in carRacers:
            car = db.session.query(Car).filter_by(id=carRacer.carId).first()
            r.cars.remove(car)

    def remove_racer_from_sponsor_association(racer_id):
        racer = db.session.query(Racer).filter_by(id=racer_id)
        r = racer.first()
        racerSponsors = db.session.query(RacerSponsor).filter_by(racerId=racer_id).all()
        for racerSponsor in racerSponsors:
            sponsor = db.session.query(Sponsor).filter_by(id=racerSponsor.sponsorId).first()
            r.sponsors.remove(sponsor)
    
    def remove_sponsor_from_racer_association(sponsor_id):
        sponsor = DataServices.get_filterBy(Sponsor, 'id', sponsor_id, True)
        racerSponsors = DataServices.get_filterBy(RacerSponsor, 'sponsorId', sponsor_id, False)
        for racerSponsor in racerSponsors:
            racer = DataServices.get_filterBy(Racer, 'id', racerSponsor.racerId, True)
            racer.sponsors.remove(sponsor)

    def get_availableRacers(email):
        availracers_list = [(0, "---")]
        if email == 'NONE':
            availRacers = db.session.query(Racer).filter(Racer.user_id == None)
            [availracers_list.append((a.id, a.name)) for a in availRacers.order_by(Racer.name).all()]
            return availracers_list
        else:
            availRacer = db.session.query(Racer).filter(Racer.email == email).first()
            if availRacer:
                [availracers_list.append((availRacer.id, availRacer.name))]
                print (availracers_list)
                return availracers_list
            else:
                availRacers = db.session.query(Racer).filter(Racer.user_id == None)
                [availracers_list.append((a.id, a.name)) for a in availRacers.order_by(Racer.name).all()]
                return availracers_list

    def remove_track_association(event_id):
        event = db.session.query(Event).filter_by(id=event_id)
        e = event.first()
        trackEvents = db.session.query(TrackEvent).filter_by(eventId=event_id).all()
        for trackEvent in trackEvents:
            track = db.session.query(Track).filter_by(id=trackEvent.trackId).first()
            e.tracks.remove(track)
    
    def get_columns(data):
        cols = sorted(data.first().keys(), key=len)
        i=0
        length = len(cols)
        while i < length:
            if 'password' in cols[i]:
                cols.remove(cols[i])
                length = length - 1
            elif 'laps' in cols[i]:
                cols.remove(cols[i])
                length = length - 1
            elif '_id' in cols[i]:
                cols.remove(cols[i])
                length = length - 1
            else:
                i = i+1
        return cols
    
    def get_form(model_name):
        if model_name == 'User':
            form = UpdateUserForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
        elif model_name == 'Track' or model_name == 'RaceClass':
            form = NameSNForm(request.form)
        elif model_name == 'Event':
            form = EventForm(request.form)
            form.tracks.choices = DataServices.get_modelChoices(Track, 'name')
        elif model_name == 'Sponsor':
            form = SponsorForm(request.form)
        elif model_name == 'Car':
            form = CarForm(request.form)
        elif model_name == 'Racer':
            form = RacerForm(request.form)
            form.cars.choices = DataServices.get_carChoices()
            form.sponsors.choices = DataServices.get_modelChoices(Sponsor, 'name')
        elif model_name == 'BestLap':
            form = BestLapForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
            form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
            form.event.choices = DataServices.get_modelChoices(Event, 'name')
        elif model_name == 'Setting':
            form = SettingsForm(request.form)
        elif model_name == 'Page':
            form = PagesForm(request.form)
        return form

class UIServices():

    def get_pghead(header):
        return header
    
    def get_rowsPerPage():
        return 10
    
    def get_modelList():
        #['User', 'Car', 'RaceClass', 'Racer', 'Track', 'Event', 'Sponsor', 'BestLap']
        return db.session.query(Page.name).all()
    
    def get_settingModelList():
        return ['Setting', 'Page']

    def get_settings():
        db_settings = DataServices.get_model(Setting)
        setting_dict = {}
        for setting in db_settings:
            setting_dict[setting.name] = setting.value

        return setting_dict