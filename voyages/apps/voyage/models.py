from django.db import models

class Voyage(models.Model):
    """
    Information about voyages.
    """

    class VoyageShip(models.Model):
        """
        Information about voyage ship.
        """
        class VoyageVentureOwner(models.Model):
            """
            Information about other owners.
            """
            number_of_owner = models.IntegerField(max_length=2)
            name_of_owner = models.CharField(max_length=40)

        class VoyageGroupings(models.Model):
            """
            Labels for groupings names.
            """
            grouping_name = models.CharField(max_length=30)

        class NationalityOfShip(models.Model):
            """
            Nationalities of ships.
            """
            nationality_of_ship = models.CharField(max_length=35)

        class TonType(models.Model):
            """
            Types of tonnage.
            """
            ton_type = models.CharField(max_length=35)

        class RigOfVessel(models.Model):
            """
            Rig of Vessel.
            """
            rig_of_vessel = models.CharField(max_length=25)


        ship_name = models.CharField("Name of vessel", max_length=60)
        national = models.ForeignKey("Country in which ship registered",
                                     NationalityOfShip)
        tonnage = models.IntegerField("Tonnage of vessel", max_length=4)
        ton_type = models.ForeignKey("Definition of ton used in tonnage",
                                     TonType)
        rig_of_vessel = models.ForeignKey("Rig of vessel", RigOfVessel)
        guns_mounted = models.IntegerField("Guns mounted", max_length=2)
        year_of_constr = models.DateField("Year of vessel's construction")
        #vessel_constr_place =
        #vessel_constr_region =
        year_of_reg = models.DateField("Year of vessel's registration")
        #reg_place =
        #reg_region =
        owner_of_venture = models.CharField("First owner of venture", max_length=60)
        owners = models.ForeignKey(VoyageVentureOwner)


    class VoyageOutcome(models.Model):
        """
        Information about Outcomes
        """

        class ParticularOutcome(models.Model):
            """
            Particular outcome.
            """
            particular_outcome = models.CharField("Outcome label", max_length=70)

        class SlavesOutcome(models.Model):
            """
            Outcome of voyage for slaves.
            """
            slaves_outcome = models.CharField("Outcome label", max_length=70)

        class VesselCapturesOutcome(models.Model):
            """
            Outcome of voyage if vessel captured.
            """
            vessel_captures_outcome = models.CharField("Outcome label",
                                                       max_length=35)

        class OwnerOutcome(models.Model):
            """
            Outcome of voyage for owner.
            """
            owner_outcome = models.CharField("Outcome label", max_length=35)

        class Resistance(models.Model):
            """
            Resistance labels
            """
            resistance_name = models.CharField("Resistance label", max_length=35)


        particular_outcome = models.ForeignKey("Particular outcome"
                                               "of voyage", ParticularOutcome)
        outcome_slaves = models.ForeignKey("Outcome of voyage for slaves",
                                             SlavesOutcome)
        vessel_captures_outcome = models.ForeignKey("Outcome of voyage"
                                                      "if vessel captured",
                                                      VesselCapturesOutcome)
        outcome_owner = models.ForeignKey("Outcome of voyage or owner",
                                            OwnerOutcome)
        resistance = models.ForeignKey("African resistance", Resistance)

