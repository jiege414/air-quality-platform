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
}
