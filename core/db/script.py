class StudentScript(object):

    get_all = "select s.ID as 'StudentID', s.Name, s.StudentNo, s.ParentName, s.ParentMobile, sf.ID as 'FeatureID', " \
              "sf.PictureName, sf.Feature " \
              "from student s " \
              "inner join StudentFeatures sf on s.ID = sf.StudentID " \
              "where s.IsExtractFeature = 0"

    get_by_id = "select * from Student where id = {}"

    update = "update Student set IsExtractFeature = {} where ID = {}"


class StudentFeaturesScript(object):

    get_by_id = "select * from StudentFeatures where ID = {}"

    update = "update StudentFeatures set Feature = '{}' where ID = {}"
