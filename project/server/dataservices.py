from project.server import db
from project.server.models import Car, CarRacer, Racer, RacerSponsor, Track, TrackEvent, \
Event, Sponsor, BestLap
# Helper Functions
class DataServices():
    
    def get_model(model_name):
        return db.session.query(model_name)

    def get_filterbyQuery(model_name, col, val):
        return db.session.query(model_name).filter_by(col=val)
    
    def get_filterbyFirstQuery(model_name, col, val):
        return db.session.query(model_name).filter_by(col=val).first()
    
    def get_carChoices():
        cars = get_cars()
        car_list = [(0, "---")]
        [car_list.append((c.id, c.number + ' ' + c.make + ' ' + c.model)) for c in cars.order_by(Car.number).all()]
        print("car_list")
        print(car_list)
        return car_list

    def get_sponsorChoices():
        sponsors = get_model(Sponsor)
        sponsor_list = [(0, "---")]
        [sponsor_list.append((s.id, s.name)) for s in sponsors.order_by(Sponsor.name).all()]
        print("sponsor_list")
        print(sponsor_list)
        return sponsor_list

    def remove_car_association(racer_id):
        racer = db.session.query(Racer).filter_by(id=racer_id)
        r = racer.first()
        carRacers = db.session.query(CarRacer).filter_by(racerId=racer_id).all()
        for carRacer in carRacers:
            car = db.session.query(Car).filter_by(id=carRacer.carId).first()
            r.cars.remove(car)

    def remove_sponsor_association(racer_id):
        racer = db.session.query(Racer).filter_by(id=racer_id)
        r = racer.first()
        racerSponsors = db.session.query(RacerSponsor).filter_by(racerId=racer_id).all()
        for racerSponsor in racerSponsors:
            sponsor = db.session.query(Sponsor).filter_by(id=racerSponsor.sponsorId).first()
            r.sponsors.remove(sponsor)

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
                return availracers_list
            else:
                availRacers = db.session.query(Racer).filter(Racer.user_id == None)
                [availracers_list.append((a.id, a.name)) for a in availRacers.order_by(Racer.name).all()]
                return availracers_list
    
    def get_trackChoices():
        tracks = get_model(Track)
        track_list = [(0, "---")]
        [track_list.append((t.id, t.name)) for t in tracks.order_by(Track.name).all()]
        return track_list

    def remove_track_association(event_id):
        event = db.session.query(Event).filter_by(id=event_id)
        e = event.first()
        trackEvents = db.session.query(TrackEvent).filter_by(eventId=event_id).all()
        for trackEvent in trackEvents:
            track = db.session.query(Track).filter_by(id=trackEvent.trackId).first()
            e.tracks.remove(track)
    
    def get_modelChoices(model_name, col):
        choices = get_model(model_name)
        choice_list = [(0, "---")]
        [choice_list.append((c.id, c.col)) for c in choices.order_by(model_name.col).all()]
        return choice_list
    

class UIServices():

    def get_pghead(header):
        return header
