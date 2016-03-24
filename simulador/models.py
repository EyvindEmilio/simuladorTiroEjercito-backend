import simple_audit
# Create your models here.

import resources.account
import resources.city
import resources.grade
import resources.people
import resources.regiment
import resources.battalion
import resources.company
import resources.squadron
import resources.military_grade
import resources.target_resource
import resources.lesson
import resources.program_practice
import resources.user_type
import resources.practices
import resources.position
import resources.type_of_fire
import resources.reset_password
import resources.results
import resources.progress
import resources.results_zone
import resources.logs
import resources.image_repository
import resources.report_repository

simple_audit.register(resources.account.Account,
                      resources.city.City,
                      resources.grade.Grade,
                      resources.military_grade.MilitaryGrade,
                      resources.target_resource.Target,
                      resources.lesson.Lesson,
                      resources.program_practice.ProgramPractice,
                      resources.user_type.UserType,
                      resources.practices.Practices,
                      resources.position.Position,
                      resources.type_of_fire.TypeOfFire,
                      resources.reset_password.ResetPassword,
                      resources.results.Results,
                      resources.results_zone.ResultsZone,
                      resources.squadron.Squadron,
                      resources.company.Company,
                      )
