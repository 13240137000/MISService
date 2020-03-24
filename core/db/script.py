class StudentScript(object):

    get_all = "select s.ID as 'StudentID', s.Name, s.StudentNo, s.ParentName, s.ParentMobile, sf.ID as 'FeatureID', " \
              "sf.PictureName, sf.Feature " \
              "from student s " \
              "inner join StudentFeatures sf on s.ID = sf.StudentID " \
              "where s.IsExtractFeature = {} and IFNULL(sf.PictureName,'') <> '' "

    get_by_id = "select * from Student where id = {}"

    get_student_by_no = "select s.*, sf.PictureName from Student s " \
                       "inner join StudentFeatures sf on s.ID = sf.StudentID " \
                       "where s.StudentNo = '{}' "

    update = "update Student set IsExtractFeature = {} where ID = {}"


class StudentFeaturesScript(object):

    get_by_id = "select * from StudentFeatures where ID = {}"

    update = "update StudentFeatures set Feature = '{}' where ID = {}"


class ErrorScript(object):

    get_all = "select e.id as 'ErrorID'," \
              "s.ID as 'StudentID', s.Name, s.StudentNo, s.ParentName,s.ParentMobile, " \
              "sf.PictureName, sf.feature " \
              "from Error e " \
              "inner join student s on e.StudentID = s.id " \
              "inner join StudentFeatures sf on e.StudentID = sf.StudentID"

    delete = "delete from Error"

    update = "insert into Error (StudentID) VALUES ({0})"

