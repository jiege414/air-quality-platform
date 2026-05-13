package com.cugb.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.cugb.entity.WarningRecord;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface WarningRecordMapper extends BaseMapper<WarningRecord> {
    
    @Select("SELECT * FROM warning_record WHERE is_handled = 0 ORDER BY create_time DESC")
    List<WarningRecord> selectUnhandledWarnings();
    
    @Select("SELECT COUNT(*) FROM warning_record WHERE is_handled = 0 AND DATE(create_time) BETWEEN #{startDate} AND #{endDate}")
    int countByDateRange(String startDate, String endDate);
    
    @org.apache.ibatis.annotations.Update("UPDATE warning_record SET is_handled = 1 WHERE is_handled = 0 AND DATE(create_time) BETWEEN #{startDate} AND #{endDate}")
    int batchHandleByDateRange(String startDate, String endDate);
    
    @Select("SELECT COUNT(*) FROM warning_record WHERE DATE(create_time) = CURDATE()")
    int countTodayWarnings();
}
